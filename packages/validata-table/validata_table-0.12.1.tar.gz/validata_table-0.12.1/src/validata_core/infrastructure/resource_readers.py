import json
from pathlib import Path
from typing import Any, List, Optional, Protocol, Sequence, Tuple, Union

import frictionless
import requests
from frictionless import formats
from frictionless.resources import TableResource

from validata_core.domain.spi import (
    FileTableService,
    InlineTableService,
    LocalDescriptorFetcher,
    RemoteDescriptorFetcher,
    RemoteTableService,
)
from validata_core.domain.types import (
    ErrType,
    Header,
    InlineData,
    Row,
    SchemaDescriptor,
    TypedException,
    ValidataResource,
    ValidationError,
)


def _extract_header_and_rows_from_resource(
    resource: TableResource,
) -> Tuple[Header, List[Row]]:
    """Extract header and data rows from frictionless source and options."""

    try:
        with resource as open_resource:
            if open_resource.cell_stream is None:
                raise ValueError("impossible de lire le contenu")

            lines: List[Sequence[Any]] = list(open_resource.read_cells())

            if not lines:
                raise ValueError("contenu vide")

            header: Header = lines[0]
            rows: List[Row] = lines[1:]

            # Fix BOM issue on first field name
            BOM_UTF8 = "\ufeff"

            if header and header[0].startswith(BOM_UTF8):
                header: Header = [header[0].replace(BOM_UTF8, "")] + list(header[1:])

        return header, rows

    except ValueError as value_error:
        raise TypedException(
            message=value_error.args[0], type=ErrType.SOURCE_ERROR
        ) from value_error

    except frictionless.exception.FrictionlessException as exception:
        validata_error = ValidationError.from_frictionless_error(exception.error, None)
        raise TypedException(
            message=validata_error.message, type=ErrType.SOURCE_ERROR
        ) from exception


class _TableToFrictionless(Protocol):
    """Generic frictionless TableResource reader, without error handling"""

    def guess_format(self) -> str: ...

    def to_table_resource(self, **options) -> TableResource: ...


class _RemoteTable(_TableToFrictionless):
    """Remote TableResource. Does not handle errors"""

    def __init__(self, url: str):
        self.url = url

    def guess_format(self) -> str:
        """guesses format from content Type Header"""

        extension_format = self._guess_format_from_extension()
        if extension_format:
            return extension_format

        content_type_header = self._guess_format_from_content_type_header()
        if content_type_header:
            return content_type_header

        default_format = "csv"
        return default_format

    def _guess_format_from_extension(self) -> str:
        suffix = Path(self.url).suffix

        if suffix.startswith("."):
            return suffix[1:]
        return ""

    def _guess_format_from_content_type_header(self) -> str:
        content_type: Optional[str] = _get_content_type_header(self.url)

        if content_type is None:
            return ""

        if content_type.startswith("text/csv"):
            return "csv"

        elif content_type.startswith("application/vnd.ms-excel"):
            return "xls"

        elif content_type.startswith("application/vnd.openxmlformats"):
            return "xlsx"

        return ""

    def to_table_resource(self, **options) -> TableResource:
        frictionless.Detector(encoding_function=_TableService.detect_encoding)
        return TableResource(self.url, **options)


class _LocalTable(_TableToFrictionless):
    """Local TableResource. Does not handle errors"""

    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content

    def guess_format(self) -> str:
        """guesses format from content Type Header"""
        file_ext = Path(self.filename).suffix.lower()
        if file_ext:
            return file_ext[1:]
        else:
            return ""

    def to_table_resource(self, **options) -> TableResource:
        return TableResource(self.content, **options)


class _TableService:
    """Generic table service to factorize code and error handling"""

    def __init__(self, table_content: _TableToFrictionless):
        self._table_content = table_content

    def _read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        table_resource = self._to_frictionless()
        return _extract_header_and_rows_from_resource(table_resource)

    def _to_frictionless(self) -> TableResource:
        format: str = self._table_content.guess_format()

        if not ValidataResource.is_supported_type(format):
            raise TypedException.new(ErrType.FORMAT_ERROR, format)

        options = {
            "format": format,
            **self.control_option(format),
            "detector": frictionless.Detector(encoding_function=self.detect_encoding),
        }

        try:
            table_resource = self._table_content.to_table_resource(**options)
        except Exception as e:
            raise TypedException.new(ErrType.SOURCE_ERROR, str(e))

        return table_resource

    @staticmethod
    def control_option(format: str) -> dict:
        # In Frictionless v5  ExcelFormat dialect is replaced by ExcelControl format,
        # see https://framework.frictionlessdata.io/docs/formats/excel.html for more information
        return (
            {"control": formats.ExcelControl(preserve_formatting=True)}
            if format == "xlsx"
            else {}
        )

    @staticmethod
    def detect_encoding(buffer: bytes) -> str:
        """Try to decode using utf-8 first, fallback on frictionless helper function."""
        try:
            buffer.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            encoding = frictionless.Detector().detect_encoding(buffer)
            return encoding.lower()


class FrictionlessFileTableService(FileTableService):
    def read_header_and_rows(
        self, filename: str, content: bytes
    ) -> Tuple[Header, List[Row]]:
        ts = _TableService(_LocalTable(filename, content))
        return ts._read_header_and_rows()


class FrictionlessRemoteTableService(RemoteTableService):
    def read_header_and_rows(self, url) -> Tuple[Header, List[Row]]:
        ts = _TableService(_RemoteTable(url))
        return ts._read_header_and_rows()


class FrictionlessInlineTableService(InlineTableService):
    def read_header_and_rows(self, data: InlineData) -> Tuple[Header, List[Row]]:
        frless_resource = self._to_frictionless(data)
        return _extract_header_and_rows_from_resource(frless_resource)

    def _to_frictionless(self, data: InlineData) -> TableResource:
        return TableResource(data)


class _ContentReader(Protocol):
    """ContentReader is an interface to classes that reads content at a given
    path"""

    def read(self, path: str) -> str: ...


class _RemoteContentReader(_ContentReader):
    """Reads remote content"""

    def read(self, path: str) -> str:
        response = requests.get(path)
        return response.text


class _LocalContentReader(_ContentReader):
    """Reads content of local file"""

    def read(self, path: str) -> str:
        with open(path) as f:
            content = f.read()
        return content


class _DescriptorFetcher:
    """Generic fetcher that deals with errors and JSON parsing"""

    _content_reader: _ContentReader
    _err_type: ErrType

    def _fetch(self, path: str) -> SchemaDescriptor:
        try:
            content = self._content_reader.read(path)
        except Exception as e:
            raise TypedException.new(self._err_type, str(e))

        schema_descriptor = _parse_json(content)
        return schema_descriptor


class LocalDescriptorReader(_DescriptorFetcher, LocalDescriptorFetcher):
    _content_reader = _LocalContentReader()
    _err_type = ErrType.LOCAL_SOURCE_ERROR

    def fetch(self, filepath: Union[str, Path]) -> SchemaDescriptor:
        return super()._fetch(str(filepath))


class RemoteDescriptorReader(_DescriptorFetcher, RemoteDescriptorFetcher):
    _content_reader = _RemoteContentReader()
    _err_type = ErrType.REMOTE_SOURCE_ERROR

    def fetch(self, url: str) -> SchemaDescriptor:
        return super()._fetch(url)


def _parse_json(content: str) -> SchemaDescriptor:
    """A simple json parsing utility functon with error handling"""
    try:
        schema_descriptor = json.loads(content)
    except Exception as e:
        raise TypedException.new(ErrType.JSON_FORMAT_ERROR, str(e))
    return schema_descriptor


def _get_content_type_header(url: str) -> Optional[str]:
    try:
        response = requests.head(url)

        return response.headers.get("Content-Type")
    except requests.RequestException:
        return None
