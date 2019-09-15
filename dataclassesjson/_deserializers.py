import dataclasses
from datetime import datetime
from typing import (  # type: ignore
    TYPE_CHECKING,
    Any,
    Dict,
    Type,
    Union,
    _GenericAlias,
)

from dataclassesjson.dataclassjson import DeserializeFields
from dataclassesjson.exceptions import DeserializationError


_ERROR_MSG = 'Invalid type={generic} for field={field}'


def set_deserialized_jsondict_fields(
    jsondict: Dict[str, Any], cls: Type[Any]
) -> None:
    fields = DeserializeFields.get_fields(cls)

    if not fields:
        fields = dataclasses.fields(cls)

    for field in fields:
        value = jsondict.get(field.name)
        jsondict[field.name] = _deserialize_field(field, value)


if TYPE_CHECKING:
    _Field = dataclasses.Field[Any]
else:
    _Field = dataclasses.Field


def _deserialize_field(field: _Field, value: Any) -> Any:
    field_type = field.type

    try:
        if isinstance(value, dict) and dataclasses.is_dataclass(field_type):
            set_deserialized_jsondict_fields(value, field_type)
            return field_type(**value)

        elif isinstance(field_type, _GenericAlias):
            return _deserialize_generic_type(field_type, field.name, value)

        elif isinstance(value, field_type):
            return value

        elif (
            isinstance(field_type, type)
            and issubclass(field_type, str)
            and isinstance(value, bytes)
        ):
            return value.decode()

        elif (
            isinstance(field_type, type)
            and issubclass(field_type, bytes)
            and isinstance(value, str)
        ):
            return value.encode()

        elif field_type is datetime:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

        elif value is None and field.default is None:
            return None

        elif field.default is not dataclasses.MISSING and value is None:
            return field_type(field.default)

        if value is not None:
            return field_type(value)

        raise DeserializationError(
            f'Required field not found error: {field.name}'
        )

    except (TypeError, ValueError) as error:
        raise DeserializationError(field.name, *error.args) from error


def _deserialize_generic_type(generic: Any, field: str, value: Any) -> Any:
    try:
        return _DESERIALIZERS_MAP[generic.__origin__](generic, field, value)
    except KeyError:
        raise DeserializationError(
            _ERROR_MSG.format(generic=generic, field=field)
        )


def _deserialize_union(generic: Any, field: str, value: Any) -> Any:
    nullable = False

    for arg in generic.__args__:
        if not isinstance(arg, type(None)):
            try:
                return arg(value)
            except TypeError:
                continue
        else:
            nullable = True

    if nullable:
        return None

    raise DeserializationError(_ERROR_MSG.format(generic=generic, field=field))


def _deserialize_list(generic: Any, field_name: str, values: Any) -> Any:
    field = dataclasses.field()
    field.name = field_name
    field.type = generic.__args__[0]

    try:
        return [_deserialize_field(field, value) for value in values]
    except TypeError as err:
        raise DeserializationError(
            _ERROR_MSG.format(generic=generic, field=field)
        ) from err


_DESERIALIZERS_MAP = {Union: _deserialize_union, list: _deserialize_list}