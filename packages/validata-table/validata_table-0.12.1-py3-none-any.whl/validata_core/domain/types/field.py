from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Union

import frictionless
import frictionless.fields as frfields

from .error_types import ErrType
from .typed_exception import TypedException


@dataclass
class FrFormatObj:
    name: str
    options: Dict[str, Any]


FrFormat = Union[str, FrFormatObj]


class FieldType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    YEAR = "year"
    YEARMONTH = "yearmonth"
    DURATION = "duration"
    GEOPOINT = "geopoint"
    GEOJSON = "geojson"
    ANY = "any"

    @classmethod
    def _missing_(cls, value):
        raise TypedException(
            "%r is not a valid field type. Valid types: %s"
            % (
                value,
                ", ".join([repr(m.value) for m in cls]),
            ),
            ErrType.FIELD_ERROR,
        )


@dataclass
class Field:
    type: FieldType
    format: str
    frless_field: frictionless.Field

    @classmethod
    def from_frictionless(cls, field: frictionless.Field) -> "Field":
        field_type_enum = FieldType(field.type)
        return Field(field_type_enum, field.format, field)

    @property
    def fr_format(self) -> Optional[FrFormat]:
        descriptor = self.frless_field.to_descriptor()

        if "frFormat" not in descriptor:
            return None

        fr_format_descriptor = descriptor["frFormat"]

        if isinstance(fr_format_descriptor, str):
            return fr_format_descriptor

        else:
            return FrFormatObj(
                fr_format_descriptor["name"],
                {k: v for k, v in fr_format_descriptor.items() if k != "name"},
            )

    @property
    def name(self) -> str:
        return self.frless_field.name

    @property
    def example(self) -> Optional[str]:
        return self.frless_field.example

    def get_true_values(self):
        assert isinstance(self.frless_field, frfields.boolean.BooleanField)
        true_values = (
            self.frless_field.true_values if self.frless_field.true_values else ["true"]
        )
        return true_values

    def get_false_values(self):
        assert isinstance(self.frless_field, frfields.boolean.BooleanField)

        false_values = (
            self.frless_field.false_values
            if self.frless_field.false_values
            else ["false"]
        )
        return false_values

    def _get_array_item_constraint(self, violated_constraint: str):
        assert isinstance(self.frless_field, frfields.array.ArrayField)
        assert self.frless_field.array_item is not None
        return self.frless_field.array_item["constraints"][violated_constraint]

    def _get_constraint(self, violated_constraint: str):
        return self.frless_field.constraints[violated_constraint]

    def get_constraint_value(self, violated_constraint: str) -> Any:
        """Extract and return constraint value from a field constraints"""

        if self.type == FieldType.ARRAY:
            return self._get_array_item_constraint(violated_constraint)

        else:
            return self._get_constraint(violated_constraint)
