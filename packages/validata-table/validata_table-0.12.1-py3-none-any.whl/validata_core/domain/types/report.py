import dataclasses
from typing import List, Optional

import frictionless

from .error import ValidationError
from .locale import Locale
from .metadata import Metadata, metadata_or_default
from .schema import Schema


@dataclasses.dataclass
class Stats:
    errors: int
    warnings: int
    seconds: float
    fields: int
    """Number of fields (columns) of the validated resource"""

    rows: int
    """Number of rows (lines) of the validated resource, excluding the header
    row"""

    rows_processed: int
    """Number of rows processed during validation.

    The validation may stop before reaching the end of the file, for instance
    if a maximum number of errors is reached.
    """

    def to_dict(self):
        return dataclasses.asdict(self)


Warning = str


class Report:
    errors: List[ValidationError]
    warnings: List[str]
    stats: Stats

    metadata: Metadata

    def __init__(
        self,
        errors: List[ValidationError],
        warnings: List[Warning],
        stats_seconds: float,
        stats_fields: int,
        stats_rows: int,
        stats_rows_processed: int,
        metadata: Optional[Metadata] = None,
    ):
        self.metadata = metadata_or_default(metadata)

        # Edit report object ihnerited frictionless.Report object's properties
        self.errors = errors
        self.warnings = warnings
        self.stats = Stats(
            len(errors),
            len(warnings),
            stats_seconds,
            stats_fields,
            stats_rows,
            stats_rows_processed,
        )

    def add_errors(self, errors: List[ValidationError]):
        """Add errors to an existing report

        Frictionless differenciates root-level errors and task errors. The
        root level argument allows to control where to add errors, despite not
        supporting multiple tasks at once in Validata.
        """

        if errors:
            self.errors.extend(errors)
            self.stats.errors += len(errors)

    def to_dict(self) -> dict:
        """Converts the report into a dict

        The output dict is JSON serializable.
        """
        return {
            "valid": self.valid,
            "stats": self.stats.to_dict(),
            "warnings": self.warnings,
            "errors": [err.to_dict() for err in self.errors],
        }

    def format(self) -> dict:
        formatted_data: dict = self.metadata.to_dict()
        formatted_data["report"] = self.to_dict()

        return formatted_data

    @property
    def valid(self) -> bool:
        return len(self.errors) == 0

    @staticmethod
    def from_frictionless_report(
        report: frictionless.Report,
        locale: Optional[Locale],
        schema: Optional[Schema],
        resource_rows: int,
    ) -> "Report":
        if report.tasks:
            task_errors = report.task.errors

            # Do not use
            # ```
            # fields = report.task.stats.get("fields")
            # ```
            # See https://github.com/frictionlessdata/frictionless-py/issues/1686
            fields = len(report.task.labels)

            rows_processed = report.task.stats.get("rows", -1)
        else:
            task_errors = []
            fields = -1
            rows_processed = -1

        all_errors = [*report.errors, *task_errors]

        return Report(
            [
                ValidationError.from_frictionless_error(e, locale, schema)
                for e in all_errors
            ],
            report.warnings,
            report.stats["seconds"],
            fields,
            resource_rows,
            rows_processed,
        )
