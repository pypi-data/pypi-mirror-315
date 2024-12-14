from typing import Any, List, Literal, Optional, Protocol, runtime_checkable

from .field import Field


class ErrorContext(Protocol):
    """Stores additional information on the error, for instance where the
    error occurred"""


@runtime_checkable
class RowContext(Protocol):
    def get_row_number(self) -> int: ...


@runtime_checkable
class FieldContext(Protocol):
    def get_field_number(self) -> int: ...

    def get_field_name(self) -> str: ...

    def get_field(self) -> Field: ...


@runtime_checkable
class CellContext(Protocol):
    def get_cell_value(self) -> Any: ...


@runtime_checkable
class ConstraintContext(Protocol):
    def get_violated_constraint(self) -> Optional[str]: ...

    def get_constraint_value(self) -> Any: ...


FieldType = Literal["date", "year", "number", "integer", "string", "boolean", "array"]


@runtime_checkable
class TypeContext(Protocol):
    def type(self) -> FieldType: ...


@runtime_checkable
class BooleanContext(Protocol):
    def get_true_values(self) -> List[str]: ...

    def get_false_values(self) -> List[str]: ...
