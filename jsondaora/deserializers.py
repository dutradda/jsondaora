import dataclasses
from datetime import datetime
from logging import getLogger
from typing import (  # type: ignore
    TYPE_CHECKING,
    Any,
    Dict,
    Type,
    Union,
    _GenericAlias,
)

from .exceptions import DeserializationError
from .fields import DeserializeFields


logger = getLogger(__name__)

_ERROR_MSG = 'Invalid type={generic} for field={field}'


def deserialize_jsondict_fields(
    jsondict: Dict[str, Any], cls: Type[Any]
) -> Dict[str, Any]:
    custom_fields = DeserializeFields.get_fields(cls)
    all_fields = dataclasses.fields(cls)
    deserialized = {}
    fields = custom_fields if custom_fields else all_fields

    for field in fields:
        value = jsondict.get(field.name)
        deserialized[field.name] = _deserialize_field(field, value)

    if custom_fields:
        for field in set(all_fields) - set(custom_fields):
            deserialized[field.name] = jsondict[field.name]

    return deserialized


if TYPE_CHECKING:
    _Field = dataclasses.Field[Any]
else:
    _Field = dataclasses.Field


def deserialize_field(
    field_name: str, field_type: Type[Any], value: Any
) -> Any:
    field = dataclasses.field()
    field.name = field_name
    field.type = field_type

    return _deserialize_field(field, value)


def _deserialize_field(field: _Field, value: Any) -> Any:
    field_type = field.type

    try:
        if isinstance(value, dict) and dataclasses.is_dataclass(field_type):
            value = deserialize_jsondict_fields(value, field_type)
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

        raise DeserializationError(field, value)

    except (TypeError, ValueError) as error:
        raise DeserializationError(field, value, error) from error


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
        if arg is not type(None):  # noqa
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
