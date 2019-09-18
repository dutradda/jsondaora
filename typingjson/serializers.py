import dataclasses
from typing import Any, Callable, Dict, Type

import orjson

from .dataclasses import asdict
from .fields import SerializeFields


def asjson(instance: Any, decoder: Any = orjson) -> bytes:
    return orjson.dumps(
        instance, default=OrjsonDefaultTypes.default_function(instance)
    )


class OrjsonDefaultTypes:
    types_default_map: Dict[Type[Any], Callable[[Any], Any]] = dict()

    @classmethod
    def set_type(cls, type_: Type[Any]) -> None:
        if not dataclasses.is_dataclass(type_):
            return

        if type_ in cls.types_default_map:
            return

        cls.types_default_map[type_] = cls._asdict_for_orjson

        for field in dataclasses.fields(type_):
            if dataclasses.is_dataclass(field.type):
                cls.types_default_map[field.type] = cls._asdict_for_orjson

    @classmethod
    def default_function(cls, instance: Any) -> Any:
        def wrap(v: Any) -> Any:
            if isinstance(v, bytes):
                return v.decode()

            return cls.types_default_map[type(v)](v)

        return wrap

    @staticmethod
    def _asdict_for_orjson(instance: Any) -> Dict[str, Any]:
        dictinst: Dict[str, Any] = asdict(instance)
        fields = SerializeFields.get_fields(type(instance))

        if not fields:
            return dictinst

        return {f.name: dictinst[f.name] for f in fields}
