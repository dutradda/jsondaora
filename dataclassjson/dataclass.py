import dataclasses
from logging import getLogger
from typing import Any, Optional, Type

from dataclassjson._typecasting import (
    _set_kwargs_generic_type,
    _typecasting_args,
)


logger = getLogger(__name__)


def dataclass(
    _cls: Optional[Type[Any]] = None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> Any:
    def wrap(cls: Type[Any]) -> Any:
        cls = dataclasses.dataclass(  # type: ignore
            cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
        )
        setattr(cls, '_dataclass_init', cls.__init__)
        setattr(cls, '__init__', _dataclassjson_init)
        setattr(cls, '_typecasting_args', _typecasting_args)
        setattr(cls, '_set_kwargs_generic_type', _set_kwargs_generic_type)

        return cls

    if _cls is None:
        return wrap

    return wrap(_cls)


def _dataclassjson_init(self: Any, *args: Any, **kwargs: Any) -> None:
    kwargs = self._typecasting_args(*args, **kwargs)
    self._dataclass_init(**kwargs)
