import logging
from pathlib import Path
from typing import List, Sequence, Tuple, Union

from validata_core.domain.spi import (
    FileTableService,
    InlineTableService,
    RemoteTableService,
)
from validata_core.domain.types import (
    Header,
    InlineData,
    Row,
    TableReader,
    Tag,
    ValidationError,
)

log = logging.Logger(__name__)


class FileContentReader(TableReader):
    def __init__(
        self, filename: Union[str, Path], content: bytes, service: FileTableService
    ):
        self._filename = str(filename)
        self._content = content
        self._service = service

    def source(self) -> str:
        return self._filename

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        return self._service.read_header_and_rows(self._filename, self._content)


class URLReader(TableReader):
    def __init__(self, url: str, service: RemoteTableService):
        self._url = url
        self._service = service

    def source(self) -> str:
        return self._url

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        return self._service.read_header_and_rows(self._url)


class InlineReader(TableReader):
    def __init__(self, data: InlineData, service: InlineTableService):
        self._data = data
        self._service = service

    def source(self) -> str:
        return "inline"

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        return self._service.read_header_and_rows(self._data)


BODY_TAGS = frozenset([Tag.BODY, Tag.CELL, Tag.CONTENT, Tag.ROW, Tag.TABLE])
STRUCTURE_TAGS = frozenset([Tag.STRUCTURE, Tag.HEADER])


def is_body_error(err: ValidationError) -> bool:
    """Classify the given error as 'body error' according to its tags."""
    tags = err.tags
    return bool(BODY_TAGS & set(tags))


def is_structure_error(err: ValidationError) -> bool:
    """Classify the given error as 'structure error' according to its tags."""
    tags = err.tags
    return bool(STRUCTURE_TAGS & set(tags))


def to_lower(str_array: Sequence[str]) -> List[str]:
    """Lower all the strings in a list"""
    return [s.lower() for s in str_array]
