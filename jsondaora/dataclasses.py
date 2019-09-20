import dataclasses
from typing import Any, Callable, Dict, List, Tuple, Type

from .deserializers import deserialize_jsondict_fields
from .exceptions import DeserializationError


def asdataclass(jsondict: Dict[str, Any], cls: Type[Any]) -> Any:
    kwargs = deserialize_jsondict_fields(jsondict, cls)

    try:
        return cls(**kwargs)
    except TypeError as err:
        raise DeserializationError(cls, jsondict) from err


def asdict(
    instance: Any, dict_factory: Callable[[List[Tuple[str, Any]]], Any] = dict
) -> Any:
    return dataclasses.asdict(instance, dict_factory=dict_factory)
