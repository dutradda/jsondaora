import dataclasses
from enum import Enum
from typing import Any, Callable, Dict, Type, _TypedDictMeta  # type: ignore

import orjson

from .fields import SerializeFields


def dataclass_asjson(instance: Any) -> bytes:
    return orjson.dumps(
        instance, default=OrjsonDefaultTypes.default_function
    )


def typed_dict_asjson(
    typed_dict: Any, typed_dict_type: _TypedDictMeta
) -> bytes:
    return orjson.dumps(
        _choose_typed_dict_fields(typed_dict, typed_dict_type),
        default=OrjsonDefaultTypes.default_function,
    )


def _choose_typed_dict_fields(
    typed_dict: Dict[str, Any], typed_dict_type: _TypedDictMeta
) -> Dict[str, Any]:
    fields = SerializeFields.get_fields(typed_dict_type)

    if not fields:
        return typed_dict

    return {
        f.name: (
            _choose_typed_dict_fields(typed_dict[f.name], f.type)
            if isinstance(typed_dict[f.name], dict)
            else typed_dict[f.name]
        )
        for f in fields
    }


class OrjsonDefaultTypes:
    types_default_map: Dict[Type[Any], Callable[[Any], Any]] = dict()

    @classmethod
    def default_function(cls, v: Any) -> Any:
        if isinstance(v, bytes):
            return v.decode()

        elif isinstance(v, Enum):
            return v.value

        elif dataclasses.is_dataclass(v):
            return cls.asdict(v)

        try:
            return cls.types_default_map[type(v)](v)
        except KeyError:
            orjson.JSONEncodeError(v)

    @staticmethod
    def asdict(instance: Any) -> Dict[str, Any]:
        dictinst: Dict[str, Any] = dataclasses.asdict(instance)
        fields = SerializeFields.get_fields(type(instance))

        if not fields:
            return dictinst

        return {f.name: dictinst[f.name] for f in fields}
