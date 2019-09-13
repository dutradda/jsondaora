import dataclasses
from typing import Any, Callable, List, Tuple


def _asdict(
    instance: Any, dict_factory: Callable[[List[Tuple[str, Any]]], Any] = dict
) -> Any:
    return dataclasses.asdict(instance, dict_factory=dict_factory)
