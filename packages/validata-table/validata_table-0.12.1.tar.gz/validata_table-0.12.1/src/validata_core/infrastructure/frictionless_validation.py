from pathlib import Path

import frictionless
from frictionless.resources import TableResource

from validata_core.domain.spi import ValidationService
from validata_core.domain.types import (
    InlineArrayOfArrays,
    Report,
    TypedException,
    ValidataResource,
)
from validata_core.domain.warning_messages import iter_warnings
from validata_core.infrastructure.resource_readers import (
    _extract_header_and_rows_from_resource,
)


class FrictionlessValidationService(ValidationService):
    def validate(self, resource, schema, checks, ignore_header_case, locale) -> Report:
        frless_schema = frictionless.Schema.from_descriptor(schema.descriptor)

        original_schema = frless_schema.to_copy()

        consolidated_resource = _consolidate_to_frless_resource(
            resource, frless_schema, ignore_header_case
        )

        source_header = None
        report = frictionless.validate(source=consolidated_resource, checks=checks)

        if report.tasks:
            try:
                source_header, _ = _extract_header_and_rows_from_resource(
                    consolidated_resource
                )
            except TypedException:
                source_header = None

        required_field_names = extract_required_field_names(frless_schema)

        for table in report.tasks:
            # Add warnings

            if source_header:
                table.warnings = list(
                    iter_warnings(
                        source_header,
                        required_field_names,
                        original_schema,
                        ignore_header_case,
                    )
                )
                table.stats["warnings"] += len(table.warnings)
                report.stats["warnings"] += len(table.warnings)
                report.warnings += table.warnings

        return Report.from_frictionless_report(report, locale, schema, resource.n_rows)

    def validate_schema(self, schema_descriptor):
        try:
            if isinstance(schema_descriptor, Path):
                schema_descriptor = str(schema_descriptor)
            frictionless.Schema.from_descriptor(schema_descriptor)
        except frictionless.FrictionlessException as exception:
            errors = exception.reasons if exception.reasons else [exception.error]
            return Report.from_frictionless_report(
                frictionless.Report.from_validation(errors=errors), None, None, 0
            )

        frictionless_report = frictionless.validate(schema_descriptor, type="schema")
        return Report.from_frictionless_report(frictionless_report, None, None, 0)


def _consolidate_to_frless_resource(
    resource: ValidataResource, schema: frictionless.Schema, ignore_header_case: bool
) -> TableResource:
    resource_data: InlineArrayOfArrays = [resource.header()] + resource.rows()

    # Merge options to pass to frictionless
    frless_resource = TableResource(
        resource_data,
        schema=schema,
        dialect=frictionless.Dialect(header_case=not ignore_header_case),
        detector=frictionless.Detector(schema_sync=True),
    )

    return frless_resource


def extract_required_field_names(
    schema: frictionless.Schema,
) -> list[str]:
    return [
        field.name
        for field in schema.fields
        if field.constraints
        and "required" in field.constraints
        and field.constraints["required"]
    ]
