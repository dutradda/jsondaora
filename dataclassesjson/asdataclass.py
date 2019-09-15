from logging import getLogger
from typing import Any, Dict, Type

from dataclassesjson._deserializers import set_deserialized_jsondict_fields


logger = getLogger(__name__)


def asdataclass(jsondict: Dict[str, Any], cls: Type[Any]) -> Any:
    set_deserialized_jsondict_fields(jsondict, cls)
    return cls(**jsondict)
