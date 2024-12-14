from pathlib import Path
from typing import Union

from validata_core.domain.helpers import FileContentReader, InlineReader, URLReader
from validata_core.domain.spi import (
    FileTableService,
    InlineTableService,
    RemoteTableService,
)
from validata_core.domain.types import InlineData, Source, ValidataResource


class ResourceFeatures:
    """Class with helper functions for creating a ValidataResource from
    various sources.
    """

    def __init__(
        self,
        file_content_service: FileTableService,
        remote_file_service: RemoteTableService,
        inline_content_service: InlineTableService,
    ):
        self._file_content_service = file_content_service
        self._remote_file_service = remote_file_service
        self._inline_content_service = inline_content_service

    def from_file_content(
        self, filename: Union[str, Path], content: bytes
    ) -> ValidataResource:
        """
        Raises:
          TypedException
        """
        return ValidataResource(
            FileContentReader(filename, content, self._file_content_service)
        )

    def from_remote_file(self, url: str) -> ValidataResource:
        """
        Raises:
          TypedException
        """
        return ValidataResource(URLReader(url, self._remote_file_service))

    def from_inline_data(self, data: InlineData) -> ValidataResource:
        """
        Raises:
          TypedException
        """
        return ValidataResource(InlineReader(data, self._inline_content_service))

    def make_validata_resource(self, source: Source) -> ValidataResource:
        """Detects the format on the source and creates the Validata Resource
        accordingly

        Raises:
          TypedException
        """
        if not isinstance(source, str) and not isinstance(source, Path):
            return self.from_inline_data(source)

        if isinstance(source, str) and source.startswith("http"):
            url = source
            return self.from_remote_file(url)
        else:
            path = source
            with open(path, "rb") as f:
                content: bytes = f.read()
            return self.from_file_content(path, content)
