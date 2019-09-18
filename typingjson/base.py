from typing import Any, Iterable, Optional, Type

from .fields import DeserializeFields, SerializeFields
from .serializers import OrjsonDefaultTypes


def typingjson(
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
