import pytest

from jsondaora.exceptions import DeserializationError
from jsondaora.schema import integer, string


def test_should_validate_minimum_integer():
    Integer = integer(minimum=10)

    with pytest.raises(DeserializationError) as exc_info:
        Integer(9)

    assert exc_info.value.args == ('Invalid minimum integer value: 10 < 9',)


def test_should_validate_maximum_integer():
    Integer = integer(maximum=9)

    with pytest.raises(DeserializationError) as exc_info:
        Integer(10)

    assert exc_info.value.args == ('Invalid maximum integer value: 10 < 9',)


def test_should_validate_min_length_string():
    String = string(min_length=2)

    with pytest.raises(DeserializationError) as exc_info:
        String('1')

    assert exc_info.value.args == ('Invalid min_length string value: 2 < 1',)


def test_should_validate_max_length_string():
    String = string(max_length=2)

    with pytest.raises(DeserializationError) as exc_info:
        String('333')

    assert exc_info.value.args == ('Invalid max_length string value: 3 < 2',)
