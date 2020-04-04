import dataclasses
from enum import Enum
from typing import Any, Dict, Set, Type

from .deserializers import deserialize_jsondict_fields
from .exceptions import DeserializationError
from .fields import SerializeFields


def asdataclass(
    jsondict: Dict[str, Any], cls: Type[Any], skip_fields: Set[str] = set()
) -> Any:
    kwargs = deserialize_jsondict_fields(jsondict, cls, skip_fields)

    try:
        return cls(**kwargs)
    except TypeError as error:
        raise DeserializationError(
            cls.__name__, jsondict, error, cls
        ) from error


def asdict(instance: Any) -> Dict[str, Any]:
    fields = SerializeFields.get_fields(type(instance))

    if not fields:
        fields = dataclasses.fields(instance)

    return {
        f.name: (
            asdict(value)
            if dataclasses.is_dataclass(
                value := getattr(instance, f.name, f.default)  # noqa
            )
            else (
                (
                    asdict(enum_value)
                    if dataclasses.is_dataclass(
                        enum_value := value.value  # noqa
                    )
                    else enum_value
                )
                if isinstance(value, Enum)
                else value
            )
        )
        for f in fields
    }
