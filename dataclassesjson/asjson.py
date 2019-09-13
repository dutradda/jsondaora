import json
from typing import Any

from .asdict import asdict
from .dataclassjson import OrjsonDefaultTypes


try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


def asjson(instance: Any, decoder: Any = orjson) -> bytes:
    if decoder is None:
        return _aspythonjson(instance)

    return _asorjson(instance)


def _asorjson(instance: Any) -> bytes:
    return orjson.dumps(
        instance, default=OrjsonDefaultTypes.default_function(instance)
    )


def _aspythonjson(instance: Any) -> bytes:
    return json.dumps(asdict(instance), separators=(',', ':')).encode()
