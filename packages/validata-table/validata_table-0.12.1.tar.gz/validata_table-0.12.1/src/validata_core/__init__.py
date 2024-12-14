import functools
from typing import Callable

from validata_core.domain.resource_features import ResourceFeatures
from validata_core.domain.schema_features import fetch_remote_descriptor
from validata_core.domain.types import Report, SchemaDescriptor
from validata_core.domain.validation_features import ValidationFeatures
from validata_core.infrastructure.fr_formats import FrFormatsRepository
from validata_core.infrastructure.frictionless_validation import (
    FrictionlessValidationService,
)
from validata_core.infrastructure.resource_readers import (
    FrictionlessFileTableService,
    FrictionlessInlineTableService,
    FrictionlessRemoteTableService,
    LocalDescriptorReader,
    RemoteDescriptorReader,
)

# Resources

file_table_service = FrictionlessFileTableService()
remote_table_service = FrictionlessRemoteTableService()
inline_table_service = FrictionlessInlineTableService()

resource_service = ResourceFeatures(
    file_table_service,
    remote_table_service,
    inline_table_service,
)

# Validation

frictionless_validation_service = FrictionlessValidationService()
remote_decriptor_fetcher = RemoteDescriptorReader()
local_descriptor_fetcher = LocalDescriptorReader()
custom_formats_repository = FrFormatsRepository()

validation_service = ValidationFeatures(
    frictionless_validation_service,
    resource_service,
    remote_decriptor_fetcher,
    local_descriptor_fetcher,
    custom_formats_repository,
)

ValidateSignature = Callable[..., Report]

validate: ValidateSignature = functools.partial(
    validation_service.validate.__func__,  # type: ignore
    validation_service,
)
validate_schema = functools.partial(
    validation_service.validate_schema.__func__,  # type: ignore
    validation_service,
)

# Schema


def fetch_remote_schema(url: str) -> SchemaDescriptor:
    return fetch_remote_descriptor(url, remote_decriptor_fetcher)
