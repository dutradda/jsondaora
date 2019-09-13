import json
from typing import Any

from ._asdict import _asdict


try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


def _asjson(instance: Any, decoder: Any = orjson) -> bytes:
    if decoder is None:
        return _aspythonjson(instance)

    return _asorjson(instance)


def _asorjson(instance: Any) -> bytes:
    return orjson.dumps(instance, default=instance.__orjson_default__)


def _aspythonjson(instance: Any) -> bytes:
    return json.dumps(_asdict(instance), separators=(',', ':')).encode()
