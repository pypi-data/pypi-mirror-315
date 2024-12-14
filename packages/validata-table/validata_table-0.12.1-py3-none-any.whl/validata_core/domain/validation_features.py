import logging
from pathlib import Path
from typing import Union

import validata_core.domain.schema_features as schema_features
from validata_core.domain.custom_checks_interface import build_custom_checks
from validata_core.domain.fr_locale import FrLocale
from validata_core.domain.resource_features import ResourceFeatures
from validata_core.domain.spi import (
    CustomFormatsRepository,
    LocalDescriptorFetcher,
    RemoteDescriptorFetcher,
    ValidationService,
)
from validata_core.domain.types import (
    Report,
    SchemaDescriptor,
    Source,
    ValidataResource,
)


class ValidationFeatures:
    def __init__(
        self,
        validation_service: ValidationService,
        resource_features: ResourceFeatures,
        remote_content_fetcher: RemoteDescriptorFetcher,
        local_content_fetcher: LocalDescriptorFetcher,
        custom_formats_repository: CustomFormatsRepository,
    ):
        self._validation_service = validation_service
        self._resource_features = resource_features
        self._remote_content_fetcher = remote_content_fetcher
        self._local_content_fetcher = local_content_fetcher
        self._custom_formats_repository = custom_formats_repository

    def validate_schema(
        self,
        schema_descriptor: SchemaDescriptor,
    ) -> Report:
        """
        Raises:
          TypedException
        """
        return self._validation_service.validate_schema(schema_descriptor)

    def validate(
        self,
        source: Source,
        schema_descriptor: Union[SchemaDescriptor, str],
        ignore_header_case: bool = False,
        locale=FrLocale(),
        **options,
    ) -> Report:
        """
        Validate a `source` using a `schema` returning a validation report.

        `source` and `schema` can be access paths to local or remote files, or
        already parsed into python.

        Raises:
          TypedException
        """

        resource: ValidataResource = self._resource_features.make_validata_resource(
            source
        )

        return self.validate_resource(
            resource, schema_descriptor, ignore_header_case, locale, **options
        )

    def validate_resource(
        self,
        resource: ValidataResource,
        schema_descriptor: Union[SchemaDescriptor, str, Path],
        ignore_header_case: bool = False,
        locale=FrLocale(),
        **options,
    ) -> Report:
        """
        Raises:
          TypedException
        """
        schema_validation_report = self._validation_service.validate_schema(
            schema_descriptor
        )

        if not schema_validation_report.valid:
            return schema_validation_report

        if isinstance(schema_descriptor, str) and schema_descriptor.startswith("http"):
            url: str = schema_descriptor
            schema_descriptor = schema_features.fetch_remote_descriptor(
                url, self._remote_content_fetcher
            )

        if isinstance(schema_descriptor, str) or isinstance(schema_descriptor, Path):
            schema_descriptor = schema_features.fetch_local_descriptor(
                schema_descriptor, self._local_content_fetcher
            )

        schema = schema_features.parse(schema_descriptor)

        # Build checks and related errors from schema
        (
            custom_checks,
            check_errors,
        ) = build_custom_checks(schema, self._custom_formats_repository)

        report: Report = self._validation_service.validate(
            resource=resource,
            schema=schema,
            checks=custom_checks,
            ignore_header_case=ignore_header_case,
            locale=locale,
        )

        report.add_errors(check_errors)

        return report


log = logging.getLogger(__name__)
