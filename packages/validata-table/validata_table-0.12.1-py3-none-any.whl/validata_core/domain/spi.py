from pathlib import Path
from typing import List, Protocol, Tuple, Union

from frictionless import Check

from validata_core.domain.types import (
    Header,
    InlineData,
    Locale,
    Report,
    Row,
    Schema,
    SchemaDescriptor,
    TypedException,
    ValidataResource,
    Validator,
)


class ValidationService(Protocol):
    def validate(
        self,
        resource: ValidataResource,
        schema: Schema,
        checks: List[Check],
        ignore_header_case: bool,
        locale: Locale,
    ) -> Report: ...

    def validate_schema(
        self, schema_descriptor: Union[SchemaDescriptor, str, Path]
    ) -> Report: ...


class FileTableService(Protocol):
    def read_header_and_rows(
        self, filename: str, content: bytes
    ) -> Tuple[Header, List[Row]]: ...


class InlineTableService(Protocol):
    def read_header_and_rows(self, data: InlineData) -> Tuple[Header, List[Row]]: ...


class RemoteTableService(Protocol):
    def read_header_and_rows(self, url: str) -> Tuple[Header, List[Row]]: ...


class TableSchemaService(Protocol):
    """Service provider interface for dealing with table schema specification"""

    def parse(self, descriptor: SchemaDescriptor) -> Union[Schema, TypedException]:
        """Parses a standard table schema descriptor into a Schema object

        All specificities of the profile (as opposed to the standard
        specification) are ignored
        """
        ...


class RemoteDescriptorFetcher(Protocol):
    def fetch(self, url: str) -> SchemaDescriptor: ...


class LocalDescriptorFetcher(Protocol):
    def fetch(self, filepath: Union[str, Path]) -> SchemaDescriptor: ...


class CustomFormatsRepository(Protocol):
    def ls(self) -> List[str]:
        """Returns a list of valid formats"""
        ...

    def get_validator(self, format: str) -> Validator:
        """Returns a validator function for the format

        Should not raise an error for an invalid format. Return `lambda x:
        True` instead"""
        ...

    def get_description(self, format: str) -> str:
        """Returns a description of the format

        Should not raise an error for an invalid format. Return an empty
        string instead"""
        ...
