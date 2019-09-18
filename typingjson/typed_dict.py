from typing import Any, Dict, Type

from .deserializers import deserialize_jsondict_fields
from .exceptions import DeserializationError


def as_typed_dict(
    jsondict: Dict[str, Any], typed_dict: Type[Dict[str, Any]]
) -> Any:
    try:
        return deserialize_jsondict_fields(jsondict, typed_dict)
    except TypeError as err:
        raise DeserializationError(typed_dict, jsondict) from err
