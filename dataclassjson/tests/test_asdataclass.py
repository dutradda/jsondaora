# type: ignore

from dataclasses import dataclass
from typing import Optional, Union

from dataclassjson import asdataclass, asjson


def tests_should_typecasting_optional_args():
    @dataclass
    class FakeDataclass:
        test: str
        test_default: Optional[int] = None

    dataclass_ = asdataclass(
        {'test': 'test', 'test_default': '1'}, FakeDataclass
    )

    assert dataclass_.test == 'test'
    assert dataclass_.test_default == 1


def tests_should_typecasting_union_args():
    @dataclass
    class FakeDataclass:
        test_union: Union[int, str]

    dataclass_ = asdataclass({'test_union': b'1'}, FakeDataclass)

    assert dataclass_.test_union == 1


def tests_should_typecasting_bytes_to_string_on_union():
    @dataclass
    class FakeDataclass:
        test_union: str

    dataclass_ = asdataclass({'test_union': b'test'}, FakeDataclass)

    assert dataclass_.test_union == 'test'


def tests_should_serialize_string():
    @dataclass
    class FakeDataclass:
        test_union: str

    dataclass_ = asdataclass({'test_union': b'test'}, FakeDataclass)

    json = asjson(dataclass_, decoder=None)

    assert json == b'{"test_union":"test"}'
