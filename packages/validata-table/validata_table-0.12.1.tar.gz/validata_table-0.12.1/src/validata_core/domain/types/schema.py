from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import frictionless

from .error_types import ErrType
from .field import Field
from .json import JSON
from .typed_exception import TypedException

SchemaDescriptor = Dict[str, JSON]


@dataclass
class CustomCheck:
    name: str
    params: Dict[str, JSON]


@dataclass
class Schema:
    descriptor: SchemaDescriptor
    fields: List[Field]
    custom_checks: List[CustomCheck]

    @classmethod
    def from_descriptor(cls, descriptor: SchemaDescriptor) -> Schema:
        try:
            schema = frictionless.Schema.from_descriptor(descriptor)
        except frictionless.FrictionlessException as e:
            raise TypedException(
                message=f"An error occurred while parsing the schema descriptor: { e }",
                type=ErrType.SCHEMA_ERROR,
            )

        custom_checks: List[CustomCheck] = []
        if "custom_checks" in descriptor:
            custom_checks = _to_custom_checks(descriptor["custom_checks"])

            schema.custom_checks = custom_checks

        return cls(
            descriptor,
            [Field.from_frictionless(f) for f in schema.fields],
            custom_checks,
        )

    def get_custom_checks(self) -> List[CustomCheck]:
        return self.custom_checks

    def get_fields(self) -> List[Field]:
        return self.fields

    def find_field_in_schema(self, field_name: str) -> Optional[Field]:
        return next(
            (field for field in self.fields if field.name == field_name),
            None,
        )


def _to_custom_checks(
    checks_descriptor: JSON,
) -> List[CustomCheck]:
    if not isinstance(checks_descriptor, List):
        raise TypedException(
            message='The "custom_checks" property expects a JSON array. Got:\n{checks_descriptor}',
            type=ErrType.CUSTOM_CHECK_ERROR,
        )

    custom_checks: List[CustomCheck] = []

    for check in checks_descriptor:
        if not isinstance(check, Dict):
            raise TypedException(
                message=f'Each element of the "custom_checks" array is expected to be a JSON object. Got:\n{check}',
                type=ErrType.CUSTOM_CHECK_ERROR,
            )

        if "name" not in check:
            raise TypedException(
                message=f'Each element custom check is expected to have a "name" property. Got:\n{check}',
                type=ErrType.CUSTOM_CHECK_ERROR,
            )

        if not isinstance(check["name"], str):
            raise TypedException(
                message=f'The "name" property of a custom check is expected to be a string. Got:\n{check["name"]}',
                type=ErrType.CUSTOM_CHECK_ERROR,
            )

        if "params" not in check:
            raise TypedException(
                message=f'Each element custom check is expected to have a "params" property. Got:\n{check}',
                type=ErrType.CUSTOM_CHECK_ERROR,
            )

        if not isinstance(check["params"], Dict):
            raise TypedException(
                message=f'The "params" property of a custom check is expected to be a JSON object. Got:\n{check["params"]}',
                type=ErrType.CUSTOM_CHECK_ERROR,
            )

        custom_checks.append(CustomCheck(check["name"], check["params"]))

    return custom_checks
