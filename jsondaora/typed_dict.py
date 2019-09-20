from typing import Any, Dict, _TypedDictMeta  # type: ignore

from .deserializers import deserialize_jsondict_fields
from .exceptions import DeserializationError


def as_typed_dict(
    jsondict: Dict[str, Any], typed_dict_type: _TypedDictMeta
) -> Any:
    try:
        return deserialize_jsondict_fields(jsondict, typed_dict_type)
    except TypeError as err:
        raise DeserializationError(typed_dict_type, jsondict) from err
