import dataclasses
from enum import Enum
from typing import Any, Dict, Set, Type

from .deserializers import deserialize_jsondict_fields
from .exceptions import DeserializationError
from .fields import SerializeFields
from .serializers import dataclass_asjson


def asdataclass(
    jsondict: Dict[str, Any],
    cls: Type[Any],
    skip_fields: Set[str] = set(),
    encode_field_name: bool = False,
) -> Any:
    kwargs = deserialize_jsondict_fields(
        jsondict, cls, skip_fields, encode_field_name
    )

    try:
        return cls(**kwargs)
    except TypeError as error:
        raise DeserializationError(
            cls.__name__, jsondict, error, cls
        ) from error


def asdict(instance: Any, dumps_value: bool = False) -> Any:
    if isinstance(instance, list) or isinstance(instance, tuple):
        return [asdict(value) for value in instance]

    elif isinstance(instance, Enum):
        return instance.value

    elif isinstance(instance, dict):
        return {
            f: dataclass_asjson(value)
            if dumps_value
            and (
                dataclasses.is_dataclass(value)
                or isinstance(value, list)
                or isinstance(value, tuple)
                or isinstance(value, dict)
            )
            else asdict(value)
            for f, value in instance.items()
        }

    elif not dataclasses.is_dataclass(instance):
        return instance

    fields = SerializeFields.get_fields(type(instance))

    if not fields:
        fields = dataclasses.fields(instance)

    return {
        f.name: dataclass_asjson(value)
        if dumps_value
        and (
            dataclasses.is_dataclass(
                value := getattr(instance, f.name, f.default)  # noqa
            )
            or isinstance(value, list)
            or isinstance(value, tuple)
            or isinstance(value, dict)
        )
        else asdict(getattr(instance, f.name, f.default))
        for f in fields
    }
