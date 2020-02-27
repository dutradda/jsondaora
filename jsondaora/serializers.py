import dataclasses
from typing import Any, Callable, Dict, Type, _TypedDictMeta  # type: ignore

import orjson

from .dataclasses import asdict
from .fields import SerializeFields


def dataclass_asjson(instance: Any) -> bytes:
    return orjson.dumps(
        instance, default=OrjsonDefaultTypes.default_function(instance)
    )


def typed_dict_asjson(
    typed_dict: Any, typed_dict_type: _TypedDictMeta
) -> bytes:
    return orjson.dumps(_choose_typed_dict_fields(typed_dict, typed_dict_type))


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
    def set_type(cls, type_: Type[Any]) -> None:
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
