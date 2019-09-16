import dataclasses
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Set,
    Type,
)

from .asdict import asdict


class OrjsonDefaultTypes:
    types_default_map: Dict[Type[Any], Callable[[Any], Any]] = dict()

    @classmethod
    def set_type(cls, type_: Type[Any]) -> None:
        if type_ in cls.types_default_map:
            return

        cls.types_default_map[type_] = _asdict_for_orjson

        for field in dataclasses.fields(type_):
            if dataclasses.is_dataclass(field.type):
                cls.types_default_map[field.type] = _asdict_for_orjson

    @classmethod
    def default_function(cls, instance: Any) -> Any:
        def wrap(v: Any) -> Any:
            if isinstance(v, bytes):
                return v.decode()

            return cls.types_default_map[type(v)](v)

        return wrap


def _asdict_for_orjson(instance: Any) -> Dict[str, Any]:
    dictinst: Dict[str, Any] = asdict(instance)
    fields = SerializeFields.get_fields(type(instance))

    if not fields:
        return dictinst

    return {f.name: dictinst[f.name] for f in fields}


class _Fields:
    if TYPE_CHECKING:
        types_fields_map: Dict[Type[Any], Set[dataclasses.Field[Any]]] = {}
    else:
        types_fields_map: Dict[Type[Any], Set[dataclasses.Field]] = {}

    @classmethod
    def set_type(cls, type_: Type[Any], field_names: Iterable[str]) -> None:
        if type_ in cls.types_fields_map:
            return

        all_fields = dataclasses.fields(type_)
        fields = (f for f in all_fields if f.name in field_names)
        cls.types_fields_map[type_] = (
            fields if isinstance(fields, set) else set(fields)
        )

    @classmethod
    def get_fields(cls, type_: Type[Any]) -> Any:
        return cls.types_fields_map.get(type_)

    @classmethod
    def clean_fields(cls, type_: Type[Any]) -> Any:
        return cls.types_fields_map.pop(type_, None)


class DeserializeFields(_Fields):
    if TYPE_CHECKING:
        types_fields_map: Dict[Type[Any], Set[dataclasses.Field[Any]]] = {}
    else:
        types_fields_map: Dict[Type[Any], Set[dataclasses.Field]] = {}


class SerializeFields(_Fields):
    if TYPE_CHECKING:
        types_fields_map: Dict[Type[Any], Set[dataclasses.Field[Any]]] = {}
    else:
        types_fields_map: Dict[Type[Any], Set[dataclasses.Field]] = {}


def dataclassjson(
    type_: Optional[Type[Any]] = None,
    deserialize_fields: Optional[Iterable[str]] = None,
    serialize_fields: Optional[Iterable[str]] = None,
) -> Any:
    def wrap(type__: Type[Any]) -> Type[Any]:
        OrjsonDefaultTypes.set_type(type__)

        if deserialize_fields is not None:
            DeserializeFields.set_type(type__, deserialize_fields)
        else:
            DeserializeFields.clean_fields(type__)

        if serialize_fields is not None:
            SerializeFields.set_type(type__, serialize_fields)
        else:
            SerializeFields.clean_fields(type__)

        return type__

    if type_:
        return wrap(type_)

    return wrap
