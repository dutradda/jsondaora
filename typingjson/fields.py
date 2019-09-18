import dataclasses
from typing import TYPE_CHECKING, Any, Dict, Iterable, Set, Type


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
