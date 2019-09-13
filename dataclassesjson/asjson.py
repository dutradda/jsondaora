import dataclasses
import json
from typing import Any, Callable, Dict, Type

from .asdict import asdict


try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


class OrjsonDefaultTypes:
    types_default_map: Dict[Type[Any], Callable[[Any], Any]] = dict()

    @classmethod
    def set_type(cls, type_: Type[Any]) -> None:
        if type_ in cls.types_default_map:
            return

        cls.types_default_map[type_] = asdict

        for field in dataclasses.fields(type_):
            if dataclasses.is_dataclass(field.type):
                cls.types_default_map[field.type] = asdict

    @classmethod
    def default_function(cls, v: Any) -> Any:
        print(type(v))
        print(cls.types_default_map)
        return cls.types_default_map[type(v)](v)


def asjson(instance: Any, decoder: Any = orjson) -> bytes:
    if decoder is None:
        return _aspythonjson(instance)

    return _asorjson(instance)


def _asorjson(instance: Any) -> bytes:
    return orjson.dumps(instance, default=OrjsonDefaultTypes.default_function)


def _aspythonjson(instance: Any) -> bytes:
    return json.dumps(asdict(instance), separators=(',', ':')).encode()


def dataclassesjson(type_: Type[Any]) -> Type[Any]:
    OrjsonDefaultTypes.set_type(type_)
    return type_
