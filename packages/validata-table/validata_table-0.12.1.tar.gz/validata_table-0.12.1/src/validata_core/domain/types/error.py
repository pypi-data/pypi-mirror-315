import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

import frictionless
from frictionless import errors as frerrors

from .context import (
    CellContext,
    ConstraintContext,
    ErrorContext,
    FieldContext,
    RowContext,
)
from .error_tags import Tag
from .error_types import ErrType
from .field import Field, FieldType
from .json import JSON
from .locale import Locale, Translation
from .schema import Schema


@dataclass
class ValidationError:
    name: str
    type: ErrType
    context: Optional[ErrorContext]
    tags: list[Tag]

    # Set to `None` for errors that are not translated
    _locale: Optional[Locale]

    _original_message: str = ""
    _original_note: str = ""

    @staticmethod
    def from_frictionless_error(
        error: frictionless.Error,
        locale: Optional[Locale],
        schema: Optional[Schema] = None,
    ) -> "ValidationError":
        class SpecificContext(ErrorContext):
            pass

        if isinstance(error, frerrors.RowError):
            setattr(SpecificContext, "get_row_number", lambda _: error.row_number)

        if isinstance(error, frerrors.CellError):
            setattr(SpecificContext, "get_cell_value", lambda _: error.cell)

        if isinstance(error, frerrors.CellError) or isinstance(
            error, frerrors.LabelError
        ):
            assert schema, "Please provide a schema to properly deal with Cell Errors"

            field = ValidationError._get_field(error, schema)
            setattr(SpecificContext, "get_field_number", lambda _: error.field_number)
            setattr(SpecificContext, "get_field_name", lambda _: error.field_name)
            setattr(SpecificContext, "get_field", lambda _: field)

            if isinstance(error, frerrors.ConstraintError):
                constraint = _extract_constraint_from_message(error)
                setattr(
                    SpecificContext,
                    "get_violated_constraint",
                    lambda _: constraint,
                )
                setattr(
                    SpecificContext,
                    "get_constraint_value",
                    lambda _: (
                        field.get_constraint_value(constraint)
                        if field and constraint
                        else ""
                    ),
                )

        context = SpecificContext()

        tags = [Tag(t) for t in error.tags]

        v = ValidationError(error.title, ErrType(error.type), context, tags, locale)
        v = _correct_schema_sync_bug(v)

        v._original_message = error.message
        v._original_note = error.note

        return v

    @staticmethod
    def _get_field(error: frictionless.Error, schema: Schema) -> Optional[Field]:
        if isinstance(error, frerrors.CellError):
            field = schema.find_field_in_schema(error.field_name)
        else:
            field = None
        return field

    @property
    def message(self):
        if self._locale:
            _, message = translate_message(self, self._locale)
            if message != "":
                return message

        return self._original_message

    @property
    def title(self):
        if self._locale:
            title, _ = translate_message(self, self._locale)
            if title != "":
                return title

        return self.name

    def to_dict(self) -> Dict[str, JSON]:
        d = {
            "message": self.message,
            "type": self.type.value,
            "tags": [tag.value for tag in self.tags],
        }

        context = self.context
        if isinstance(context, RowContext):
            d["rowNumber"] = context.get_row_number()

        if isinstance(context, FieldContext):
            d["fieldName"] = context.get_field_name()
            d["fieldNumber"] = context.get_field_number()

        if isinstance(context, CellContext):
            d["cell"] = context.get_cell_value()

        return d


CONSTRAINT_RE = re.compile(r'^constraint "([^"]+)" is .*$')
ARRAY_CONSTRAINT_RE = re.compile(r'^array item constraint "([^"]+)" is .*$')


def _extract_constraint_from_message(err: frerrors.Error) -> Optional[str]:
    m = CONSTRAINT_RE.match(err.note) or ARRAY_CONSTRAINT_RE.match(err.note)

    return m[1] if m else None


def translate_message(err: ValidationError, locale: Locale) -> Translation:
    ctx = err.context

    if err.type == ErrType.EXTRA_CELL:
        assert isinstance(ctx, RowContext)
        return locale.extra_cell(ctx.get_row_number())

    elif err.type == ErrType.TYPE_ERROR:
        assert isinstance(ctx, FieldContext)
        assert isinstance(ctx, CellContext)

        field_def = ctx.get_field()

        return _type_error(ctx.get_cell_value(), locale, field_def)

    elif err.type == ErrType.CONSTRAINT_ERROR:
        assert isinstance(ctx, FieldContext)
        field_def = ctx.get_field()
        return _constraint_error(err, locale, field_def)

    elif err.type == ErrType.MISSING_CELL:
        return locale.missing_cell()

    elif err.type == ErrType.UNIQUE_ERROR:
        return locale.unique_error()

    elif err.type == ErrType.TRUNCATED_VALUE:
        return locale.truncated_value()

    elif err.type == ErrType.FORBIDDEN_VALUE:
        return locale.forbidden_value()

    elif err.type == ErrType.SEQUENTIAL_VALUE:
        return locale.sequential_value()

    elif err.type == ErrType.ASCII_VALUE:
        return locale.ascii_value()

    # Label errors

    elif err.type == ErrType.BLANK_HEADER:
        assert isinstance(ctx, FieldContext)
        return locale.blank_header(ctx.get_field_number())

    elif err.type == ErrType.DUPLICATE_LABEL:
        return locale.duplicate_labels()

    elif err.type == ErrType.MISSING_LABEL:
        assert isinstance(ctx, FieldContext)
        return locale.missing_label(ctx.get_field_name())

    # Resource errors

    elif err.type == ErrType.ENCODING_ERROR:
        return locale.encoding(err._original_note)

    # Row errors

    elif err.type == ErrType.BLANK_ROW:
        assert isinstance(ctx, RowContext)
        return locale.blank_row(ctx.get_row_number())

    elif err.type == ErrType.PRIMARY_KEY:
        return locale.primary_key()

    elif err.type == ErrType.FOREIGN_KEY:
        return locale.foreign_key()

    elif err.type == ErrType.DUPLICATE_ROW:
        return locale.duplicate_row()

    elif err.type == ErrType.ROW_CONSTRAINT:
        return locale.row_constraint()

    return "", ""


def _type_error(
    field_value: Any, locale: Locale, field_def: Optional[Field]
) -> Translation:
    """Return french name and french message related to
    'type' frictionless error.
    """

    if field_def is None:
        return "", ""

    if field_def.type == FieldType.DATE:
        return locale.date_type(field_value, field_def.format)

    elif field_def.type == FieldType.YEAR:
        return locale.year_type(field_value)

    elif field_def.type == FieldType.NUMBER:
        return locale.number_type(field_value)

    elif field_def.type == FieldType.INTEGER:
        return locale.integer_type(field_value)

    elif field_def.type == FieldType.STRING:
        return locale.string_type(field_def.format)

    elif field_def.type == FieldType.BOOLEAN:
        return locale.boolean_type(
            field_def.get_true_values(), field_def.get_false_values()
        )

    else:
        return ("Erreur interne", "Cette erreur ne devrait jamais arriver")


def _constraint_error(
    err: ValidationError, locale: Locale, field_def: Field
) -> Translation:
    """Return french message related to 'constraint' frictionless error."""

    context = err.context

    assert isinstance(context, ConstraintContext)

    c = context.get_violated_constraint()

    constraint_val = context.get_constraint_value()

    if c == "required":
        return locale.required()

    if c == "unique":
        return locale.unique()

    if c == "minLength":
        assert isinstance(context, CellContext)
        cell = context.get_cell_value()
        return locale.min_length(cell, constraint_val)

    if c == "maxLength":
        assert isinstance(context, CellContext)
        cell = context.get_cell_value()
        return locale.max_length(cell, constraint_val)

    if c == "minimun":
        assert isinstance(context, CellContext)
        cell = context.get_cell_value()
        return locale.minimum(cell, constraint_val)

    if c == "maximum":
        assert isinstance(context, CellContext)
        cell = context.get_cell_value()
        return locale.maximum(cell, constraint_val)

    if c == "pattern":
        assert isinstance(context, CellContext)

        cell = context.get_cell_value()
        return locale.pattern(cell, field_def.example or "", constraint_val)

    if c == "enum":
        return locale.enum(constraint_val)

    return _unknown_constraint_error(err)


def _unknown_constraint_error(err: ValidationError) -> Translation:
    return "Contrainte non repectée", err._original_note


def _correct_schema_sync_bug(err: ValidationError) -> ValidationError:
    """With the `schema_sync` option, an untyped error can be returned. This
    function corrects the error type.

    This is an upstream bug, related to https://github.com/frictionlessdata/frictionless-py/issues/1339
    """
    if err._original_message == '"schema_sync" requires unique labels in the header':
        err.type = ErrType.DUPLICATE_LABEL
    return err
