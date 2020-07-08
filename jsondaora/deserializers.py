import dataclasses
from datetime import datetime
from logging import getLogger
from typing import (  # type: ignore
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Set,
    Type,
    Union,
    _GenericAlias,
)

import orjson

from .exceptions import DeserializationError
from .fields import DeserializeFields


logger = getLogger(__name__)

_ERROR_MSG = 'Invalid type={annotation} for field={field_name}'


def deserialize_jsondict_fields(
    jsondict: Union[Dict[str, Any], Dict[bytes, Any]],
    cls: Type[Any],
    skip_fields: Set[str] = set(),
    has_bytes_keys: bool = False,
) -> Dict[str, Any]:
    custom_fields = DeserializeFields.get_fields(cls)
    all_fields = dataclasses.fields(cls)
    deserialized = {}
    fields = custom_fields if custom_fields else all_fields
    skipped_fields = set()

    if skip_fields:
        new_fields = set()
        for f in fields:
            if f.name in skip_fields:
                skipped_fields.add(f)
            else:
                new_fields.add(f)
        fields = new_fields

    if has_bytes_keys:
        for field in fields:
            value = jsondict.get(field.name.encode())
            deserialized[field.name] = deserialize_field(
                field_name=field.name,
                field_type=field.type,
                field_default=field.default,
                value=value,
                cls=cls,
            )
    else:
        for field in fields:
            value = jsondict.get(field.name)
            deserialized[field.name] = deserialize_field(
                field_name=field.name,
                field_type=field.type,
                field_default=field.default,
                value=value,
                cls=cls,
            )

    if custom_fields or skipped_fields:
        for field in (
            set(all_fields) - custom_fields if custom_fields else set()
        ).union(skipped_fields):
            deserialized[field.name] = jsondict[field.name]

    return deserialized


if TYPE_CHECKING:
    _Field = dataclasses.Field[Any]
else:
    _Field = dataclasses.Field


def deserialize_field(
    field_name: str,
    field_type: Any,
    value: Any,
    cls: Optional[Type[Any]] = None,
    field_default: Any = dataclasses.MISSING,
) -> Any:
    try:
        if hasattr(field_type, '__get_dynamic_type__'):
            dynamic_type = field_type.__get_dynamic_type__(value)
            return deserialize_field(
                field_name=field_name,
                field_type=dynamic_type,
                value=value,
                cls=cls,
                field_default=field_default,
            )

        elif isinstance(value, dict) and dataclasses.is_dataclass(field_type):
            value = deserialize_jsondict_fields(value, field_type)
            return field_type(**value)

        elif (isinstance(value, bytes) or isinstance(value, str)) and (
            dataclasses.is_dataclass(field_type)
            or (
                isinstance(field_type, _GenericAlias)
                and (
                    field_type.__origin__ is dict
                    or field_type.__origin__ is list
                    or field_type.__origin__ is tuple
                )
            )
        ):
            return deserialize_field(
                field_name=field_name,
                field_type=field_type,
                value=orjson.loads(value),
                cls=cls,
                field_default=field_default,
            )

        elif isinstance(field_type, _GenericAlias):
            return _deserialize_generic_type(field_type, field_name, value)

        if field_type is Any:
            return value

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

        if field_type is bool:
            return value in (b'1', 1, '1', 't', 'true', 'y', 'yes')

        elif value is None and field_default is None:
            return None

        elif field_default is not dataclasses.MISSING and value is None:
            return field_type(field_default)

        if value is not None:
            return field_type(value)

        raise DeserializationError(
            field_name, field_type, field_default, value, cls
        )

    except (TypeError, ValueError) as error:
        raise DeserializationError(
            field_name, field_type, field_default, value, cls
        ) from error


def _deserialize_generic_type(
    generic: Any, field_name: str, value: Any
) -> Any:
    try:
        return _DESERIALIZERS_MAP[generic.__origin__](
            generic, field_name, value
        )
    except KeyError:
        raise DeserializationError(
            _ERROR_MSG.format(annotation=generic, field_name=field_name)
        )


def _deserialize_union(generic: Any, field_name: str, value: Any) -> Any:
    nullable = False
    has_error = False

    for type_ in generic.__args__:
        if type_ is not type(None):  # noqa
            if value is not None:
                try:
                    return deserialize_field(
                        field_name=field_name,
                        field_type=type_,
                        value=value,
                        cls=generic,
                    )
                except DeserializationError:
                    has_error = True
                    continue
        else:
            nullable = True

    if nullable and not has_error:
        return None

    raise DeserializationError(
        _ERROR_MSG.format(annotation=generic, field_name=field_name)
    )


def _deserialize_list(annotation: Any, field_name: str, values: Any) -> Any:
    try:
        return [
            deserialize_field(
                field_name=field_name,
                field_type=annotation.__args__[0],
                value=value,
                cls=annotation,
            )
            for value in values
        ]
    except TypeError as err:
        raise DeserializationError(
            _ERROR_MSG.format(annotation=annotation, field_name=field_name)
        ) from err


def _deserialize_tuple(annotation: Any, field_name: str, values: Any) -> Any:
    try:
        if annotation.__args__[-1] is ...:
            return tuple(
                deserialize_field(
                    field_name=field_name,
                    field_type=annotation.__args__[0],
                    value=value,
                    cls=annotation,
                )
                for value in values
            )

        elif len(annotation.__args__) == len(values):
            return tuple(
                deserialize_field(
                    field_name=field_name,
                    field_type=annotation.__args__[i],
                    value=value,
                    cls=annotation,
                )
                for i, value in enumerate(values)
            )

        else:
            raise DeserializationError(
                _ERROR_MSG.format(annotation=annotation, field_name=field_name)
            )

    except TypeError as err:
        raise DeserializationError(
            _ERROR_MSG.format(annotation=annotation, field_name=field_name)
        ) from err


def _deserialize_set(annotation: Any, field_name: str, values: Any) -> Any:
    try:
        return set(
            deserialize_field(
                field_name=field_name,
                field_type=annotation.__args__[0],
                value=value,
                cls=annotation,
            )
            for value in values
        )
    except TypeError as err:
        raise DeserializationError(
            _ERROR_MSG.format(annotation=annotation, field_name=field_name)
        ) from err


def _deserialize_dict(annotation: Any, field_name: str, values: Any) -> Any:
    new_dict: Dict[Any, Any] = {}

    try:
        for i, (key, value) in enumerate(values.items()):
            new_dict[
                deserialize_field(
                    field_name=f'{field_name}.key{i}',
                    field_type=annotation.__args__[0],
                    value=key,
                    cls=annotation,
                )
            ] = deserialize_field(
                field_name=f'{field_name}.value{i}',
                field_type=annotation.__args__[1],
                value=value,
                cls=annotation,
            )

    except (TypeError, AttributeError) as err:
        raise DeserializationError(
            _ERROR_MSG.format(annotation=annotation, field_name=field_name)
        ) from err

    else:
        return new_dict


_DESERIALIZERS_MAP = {
    Union: _deserialize_union,
    list: _deserialize_list,
    tuple: _deserialize_tuple,
    set: _deserialize_set,
    dict: _deserialize_dict,
}
