from typing import Any, Dict, Type

from dataclassesjson._deserializers import set_deserialized_jsondict_fields
from dataclassesjson.exceptions import DeserializationError


def asdataclass(jsondict: Dict[str, Any], cls: Type[Any]) -> Any:
    set_deserialized_jsondict_fields(jsondict, cls)

    try:
        return cls(**jsondict)
    except TypeError as err:
        raise DeserializationError(cls, jsondict) from err
