import pytest

from jsondaora.exceptions import DeserializationError
from jsondaora.schema import IntegerField, StringField


def test_should_validate_minimum_integer():
    class Integer(IntegerField, minimum=10):
        ...

    with pytest.raises(DeserializationError) as exc_info:
        Integer(9)

    assert exc_info.value.args == ('Invalid minimum integer value: 10 < 9',)


def test_should_validate_maximum_integer():
    class Integer(IntegerField, maximum=9):
        ...

    with pytest.raises(DeserializationError) as exc_info:
        Integer(10)

    assert exc_info.value.args == ('Invalid maximum integer value: 10 < 9',)


def test_should_validate_min_length_string():
    class String(StringField, min_length=2):
        ...

    with pytest.raises(DeserializationError) as exc_info:
        String('1')

    assert exc_info.value.args == ('Invalid min_length string value: 2 < 1',)


def test_should_validate_max_length_string():
    class String(StringField, max_length=2):
        ...

    with pytest.raises(DeserializationError) as exc_info:
        String('333')

    assert exc_info.value.args == ('Invalid max_length string value: 3 < 2',)
