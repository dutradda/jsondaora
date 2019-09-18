from types import MethodType
from typing import Any, Callable, Dict, Optional, Sequence, Type

from .exceptions import DeserializationError


def string(
    max_length: Optional[int] = None, min_length: Optional[int] = None
) -> 'StringField':
    if max_length is None and min_length is None:
        return str  # type: ignore

    return StringMeta(  # type: ignore
        'StringField',
        (StringField,),
        {'max_length': max_length, 'min_length': min_length},
    )


def integer(
    maximum: Optional[int] = None, minimum: Optional[int] = None
) -> 'IntegerField':
    if maximum is None and minimum is None:
        return int  # type: ignore

    return IntegerMeta(  # type: ignore
        'IntegerField',
        (IntegerField,),
        {'maximum': maximum, 'minimum': minimum},
    )


class JsonField:
    ...


class StringField(JsonField):
    max_length: int
    min_length: int
    value: str

    def __init__(self, value: Any):
        self.value = str(value)
        type(self).validate(self.value)  # type: ignore


class IntegerField(JsonField):
    maximum: int
    minimum: int

    def __init__(self, value: Any):
        self.value = int(value)
        type(self).validate(self.value)  # type: ignore


class StringMeta(type):
    def __init__(
        cls, name: str, bases: Sequence[Type[Any]], attrs: Dict[str, Any]
    ):
        cls.max_length = attrs.get('max_length')
        cls.min_length = attrs.get('min_length')

        if cls.max_length is None and cls.min_length is not None:
            cls.validate = MethodType(validate_min_length, cls)

        elif cls.max_length is not None and cls.min_length is None:
            cls.validate = MethodType(validate_max_length, cls)

        elif cls.max_length is not None and cls.min_length is not None:
            cls.validate = MethodType(validate_min_length_max_length, cls)


class IntegerMeta(type):
    maximum: int
    minimum: int
    validate: Callable[['IntegerMeta', int], bool]

    def __init__(
        cls, name: str, bases: Sequence[Type[Any]], attrs: Dict[str, Any]
    ):
        cls.maximum = attrs.get('maximum')  # type: ignore
        cls.minimum = attrs.get('minimum')  # type: ignore

        if cls.maximum is None and cls.minimum is not None:
            cls.validate = MethodType(validate_minimum, cls)

        elif cls.maximum is not None and cls.minimum is None:
            cls.validate = MethodType(validate_maximum, cls)

        elif cls.maximum is not None and cls.minimum is not None:
            cls.validate = MethodType(  # type: ignore
                validate_minimum_maximum, cls
            )


def validate_minimum(cls: IntegerMeta, value: int) -> None:
    if not cls.minimum <= value:
        raise DeserializationError(
            f'Invalid minimum integer value: {cls.minimum} < {value}'
        )


def validate_maximum(cls: IntegerMeta, value: int) -> None:
    if not cls.maximum >= value:
        raise DeserializationError(
            f'Invalid maximum integer value: {value} < {cls.maximum}'
        )


def validate_minimum_maximum(cls: IntegerMeta, value: int) -> None:
    if not cls.minimum <= value <= cls.maximum:
        raise DeserializationError(
            f'Invalid minimum and maximum integer value: '
            f'{cls.minimum} < {value} < {cls.maximum}'
        )


def validate_min_length(cls: StringMeta, value: str) -> None:
    if not cls.min_length <= len(value):  # type: ignore
        raise DeserializationError(
            f'Invalid min_length string value: {cls.min_length} < {len(value)}'
        )


def validate_max_length(cls: StringMeta, value: str) -> None:
    if not cls.max_length >= len(value):  # type: ignore
        raise DeserializationError(
            f'Invalid max_length string value: {len(value)} < {cls.max_length}'
        )


def validate_min_length_max_length(cls: StringMeta, value: str) -> None:
    if not cls.min_length <= len(value) <= cls.max_length:  # type: ignore
        raise DeserializationError(
            f'Invalid min_length and max_length string value: '
            f'{cls.min_length} < {len(value)} < {cls.max_length}'
        )
