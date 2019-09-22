import dataclasses
from typing import Any, Callable, Dict, List, Set, Tuple, Type

from .deserializers import deserialize_jsondict_fields
from .exceptions import DeserializationError


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


def asdict(
    instance: Any, dict_factory: Callable[[List[Tuple[str, Any]]], Any] = dict
) -> Any:
    return dataclasses.asdict(instance, dict_factory=dict_factory)
