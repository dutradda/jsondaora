from types import MethodType
from typing import Any, Callable, Optional, Type

from dictdaora import DictDaora

from .exceptions import DeserializationError


class StringField(DictDaora):
    max_length: int
    min_length: int
    value: str
    validate: Callable[[Type['StringField'], str], None]

    def __init__(self, value: Any):
        self.value = str(value)
        type(self).validate(self.value)  # type: ignore

    def __init_subclass__(
        cls, min_length: Optional[int] = None, max_length: Optional[int] = None
    ) -> None:
        if max_length is None and min_length is not None:
            cls.validate = MethodType(validate_min_length, cls)

        elif max_length is not None and min_length is None:
            cls.validate = MethodType(validate_max_length, cls)

        elif max_length is not None and min_length is not None:
            cls.validate = MethodType(validate_min_length_max_length, cls)

        elif min_length is None and max_length is None:
            cls.validate = MethodType(lambda c, v: v, cls)

        if min_length is not None:
            cls.min_length = min_length

        if max_length is not None:
            cls.max_length = max_length


class IntegerField(DictDaora):
    maximum: int
    minimum: int
    value: int
    validate: Callable[[Type['IntegerField'], int], None]

    def __init__(self, value: Any):
        self.value = int(value)
        type(self).validate(self.value)  # type: ignore

    def __init_subclass__(
        cls, minimum: Optional[int] = None, maximum: Optional[int] = None
    ) -> None:
        if maximum is None and minimum is not None:
            cls.validate = MethodType(validate_minimum, cls)

        elif maximum is not None and minimum is None:
            cls.validate = MethodType(validate_maximum, cls)

        elif maximum is not None and minimum is not None:
            cls.validate = MethodType(validate_minimum_maximum, cls)

        elif maximum is None and minimum is None:
            cls.validate = MethodType(lambda c, v: v, cls)

        if minimum is not None:
            cls.minimum = minimum

        if maximum is not None:
            cls.maximum = maximum


def validate_minimum(cls: Type[IntegerField], value: int) -> None:
    if not cls.minimum <= value:
        raise DeserializationError(
            f'Invalid minimum integer value: {cls.minimum} < {value}'
        )


def validate_maximum(cls: Type[IntegerField], value: int) -> None:
    if not cls.maximum >= value:
        raise DeserializationError(
            f'Invalid maximum integer value: {value} < {cls.maximum}'
        )


def validate_minimum_maximum(cls: Type[IntegerField], value: int) -> None:
    if not cls.minimum <= value <= cls.maximum:
        raise DeserializationError(
            f'Invalid minimum and maximum integer value: '
            f'{cls.minimum} < {value} < {cls.maximum}'
        )


def validate_min_length(cls: Type[StringField], value: str) -> None:
    if not cls.min_length <= len(value):
        raise DeserializationError(
            f'Invalid min_length string value: {cls.min_length} < {len(value)}'
        )


def validate_max_length(cls: Type[StringField], value: str) -> None:
    if not cls.max_length >= len(value):
        raise DeserializationError(
            f'Invalid max_length string value: {len(value)} < {cls.max_length}'
        )


def validate_min_length_max_length(cls: Type[StringField], value: str) -> None:
    if not cls.min_length <= len(value) <= cls.max_length:
        raise DeserializationError(
            f'Invalid min_length and max_length string value: '
            f'{cls.min_length} < {len(value)} < {cls.max_length}'
        )
