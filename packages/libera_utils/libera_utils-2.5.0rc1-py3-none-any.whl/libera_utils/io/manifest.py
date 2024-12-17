"""Module for manifest file handling"""
# Standard
import json
import logging
import warnings
from datetime import datetime, timezone
from hashlib import md5
from pathlib import Path
from typing import Union, Optional, Any, Annotated

# Installed
from cloudpathlib import S3Path, AnyPath
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer
from ulid import ULID

# Local
from libera_utils.aws.constants import ManifestType
from libera_utils.io.filenaming import ManifestFilename, AbstractValidFilename
from libera_utils.io.smart_open import smart_open

logger = logging.getLogger(__name__)


class ManifestError(Exception):
    """Generic exception related to manifest file handling"""
    pass


def calculate_checksum(file: Union[str, Path, S3Path]) -> str:
    """Compute the checksum of the given file."""
    with smart_open(file, 'rb') as fh:
        checksum_calculated = md5(fh.read(), usedforsecurity=False).hexdigest()
    return checksum_calculated


def get_ulid_code(filename: Optional[Union[str, Path, S3Path, ManifestFilename]]) -> Optional[ULID]:
    """Get ULID code from filename."""
    if not filename:
        return None
    if isinstance(filename, ManifestFilename):
        return filename.filename_parts.ulid_code
    return AbstractValidFilename.from_file_path(filename).filename_parts.ulid_code

class ManifestFileStructure(BaseModel):
    """Pydantic model for an individual data file listed within a manifest file."""
    filename: str = Field(description="Manifest file name")
    checksum: str = Field(description="Manifest file checksum, calculated if not provided")


class Manifest(BaseModel):
    """Pydantic model for a manifest file."""
    manifest_type: ManifestType = Field(
        description="Either INPUT or OUTPUT."
    )
    # using Annotated here avoids a pylint no-member error when appending to files list
    files: Annotated[list[ManifestFileStructure], Field(
        default_factory=list,
        description="List of ManifestFileStructure."
    )]
    configuration: dict[str, Any] = Field(
        description="Freeform json-compatible dictionary of configuration items."
    )
    filename: Optional[Union[str, Path, S3Path, ManifestFilename]] = Field(
        default=None,
        description="Preset filename, optional."
    )
    ulid_code: ULID = Field(
        default_factory=lambda data: get_ulid_code(data['filename']),
        description="ULID code from input filename."
    )

    @field_validator("files", mode="before")  # noqa  avoid type warning
    @classmethod
    def transform_files(
            cls,
            raw_list: Optional[list[Union[str, Path, S3Path, ManifestFileStructure]]]
    ) -> list[ManifestFileStructure]:
        """Allow for the incoming files list to have varying types.
        Convert to a standardized list of ManifestFileStructure."""
        result = []
        for raw_file in raw_list or []:
            if isinstance(raw_file, ManifestFileStructure):
                file_structure = raw_file
            elif isinstance(raw_file, dict):
                file_structure = ManifestFileStructure(
                    filename=raw_file.get("filename"),
                    checksum=raw_file.get("checksum") or calculate_checksum(raw_file.get("filename")),
                )
            else:
                file_structure = ManifestFileStructure(
                    filename=str(AnyPath(raw_file)),
                    checksum=calculate_checksum(raw_file)
                )
            result.append(file_structure)
        return result

    @field_serializer('filename')
    def serialize_filename(
            self,
            filename: Optional[Union[str, Path, S3Path, ManifestFilename]],
            _info
    ) -> str:
        """Custom serializer for the manifest filename."""
        return str(filename)

    model_config = ConfigDict(
        # Allow using ManifestFilename as a field
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_file(cls, filepath: Union[str, Path, S3Path]):
        """Read a manifest file and return a Manifest object (factory method).

        Parameters
        ----------
        filepath : Union[str, Path, S3Path]
            Location of manifest file to read.

        Returns
        -------
        Manifest
            Pydantic model built from the json of the given manifest file.
        """
        with smart_open(filepath) as manifest_file:
            contents = json.loads(manifest_file.read())
        contents['filename'] = filepath
        return Manifest.model_validate(contents)

    def add_files(self, *files: Union[str, Path, S3Path]):
        """Add files to the manifest from filename

        Parameters
        ----------
        files : Union[str, Path, S3Path]
            Path to the file to add to the manifest.

        Returns
        -------
        None
        """
        # get existing files and checksums as sets to check for duplicates
        existing_names = set()
        existing_checksums = set()
        for f in self.files:
            existing_names.add(f.filename)
            existing_checksums.add(f.checksum)

        for file in files:
            # S3 paths are always absolute so this is always valid for them
            if not AnyPath(file).is_absolute():
                raise ValueError(f"The file path for {AnyPath(file)} must be an absolute path.")
            if str(AnyPath(file)) in existing_names:
                warnings.warn(f"Attempting to add {file} to manifest {self} but it is already included.")
                continue
            checksum_calculated = calculate_checksum(file)
            if checksum_calculated in existing_checksums:
                warnings.warn(f"Attempting to add {file} to manifest {self} but another file with "
                              f"the same checksum is already included.")
            file_structure = ManifestFileStructure(filename=str(file), checksum=checksum_calculated)
            self.files.append(file_structure)
            existing_names.add(str(AnyPath(file)))
            existing_checksums.add(checksum_calculated)

    def validate_checksums(self) -> None:
        """Validate checksums of listed files"""
        # Note: any gzipped file will be opened and read by smart_open so the checksum reflects the data
        # in the zipped file not the zipped file itself.
        failed_filenames = []
        for file_structure in self.files:
            checksum_expected = file_structure.checksum
            filename = file_structure.filename
            checksum_calculated = calculate_checksum(filename)
            if checksum_expected != checksum_calculated:
                logger.error(f"Checksum validation for {filename} failed. "
                             f"Expected {checksum_expected} but got {checksum_calculated}.")
                failed_filenames.append(str(filename))
        if failed_filenames:
            raise ValueError(f"Files failed checksum validation: {', '.join(failed_filenames)}")

    def _generate_filename(self) -> ManifestFilename:
        """Generate a valid manifest filename"""
        mfn = ManifestFilename.from_filename_parts(
            manifest_type=self.manifest_type,
            ulid_code=ULID.from_datetime(datetime.now(timezone.utc))
        )
        return mfn

    def write(self, out_path: Union[str, Path, S3Path], filename: str = None) -> Union[Path, S3Path]:
        """Write a manifest file from a Manifest object (self).

        Parameters
        ----------
        out_path : Union[str, Path, S3Path]
            Directory path to write to (directory being used loosely to refer also to an S3 bucket path).
        filename : str, Optional
            must be a valid manifest filename.
            If not provided, the method uses the objects internal filename attribute. If that is
            not set, then a filename is automatically generated.

        Returns
        -------
        Union[Path, S3Path]
            The path where the manifest file is written.
        """
        if filename is None:
            filename = self._generate_filename() if self.filename is None else self.filename
        else:
            filename = ManifestFilename(filename)
        filepath = AnyPath(out_path) / filename.path

        # Update object's filename to the filepath we just wrote
        self.filename = ManifestFilename(filepath)

        with smart_open(self.filename.path, 'x') as manifest_file:
            manifest_file.write(self.model_dump_json())
        return self.filename.path

    def add_desired_time_range(self, start_datetime: datetime, end_datetime: datetime):
        """Add a time range to the configuration section of the manifest.

        Parameters
        ----------
        start_datetime : datetime.datetime
            The desired start time for the range of data in this manifest

        end_datetime : datetime.datetime
            The desired end time for the range of data in this manifest

        Returns
        -------
        None
        """
        self.configuration["start_time"] = start_datetime.strftime('%Y-%m-%d:%H:%M:%S')
        self.configuration["end_time"] = end_datetime.strftime('%Y-%m-%d:%H:%M:%S')

    @classmethod
    def output_manifest_from_input_manifest(
            cls,
            input_manifest: Union[Path, S3Path, 'Manifest']
    ) -> 'Manifest':
        """ Create Output manifest from input manifest file path, adds input files to output manifest configuration

        Parameters
        ----------
        input_manifest : Union[Path, S3Path, 'Manifest']
            An S3 or regular path to an input_manifest object, or the input manifest object itself

        Returns
        -------
        output_manifest : Manifest
            The newly created output manifest
        """

        if not isinstance(input_manifest, cls):
            input_manifest = Manifest.from_file(input_manifest)

        input_filename = input_manifest.filename
        if not isinstance(input_filename, AbstractValidFilename):
            input_filename = AbstractValidFilename.from_file_path(input_filename)
        input_manifest_ulid_code = input_filename.filename_parts.ulid_code

        output_filename = ManifestFilename.from_filename_parts(manifest_type=ManifestType.OUTPUT,
                                                               ulid_code=input_manifest_ulid_code)

        output_manifest = Manifest(manifest_type=ManifestType.OUTPUT,
                                   filename=output_filename,
                                   configuration={'input_manifest_files': input_manifest.files})

        return output_manifest
