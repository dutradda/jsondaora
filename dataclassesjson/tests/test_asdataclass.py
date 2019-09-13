# type: ignore

from dataclasses import dataclass
from typing import Optional, Union

from dataclassesjson import asdataclass, asjson, dataclassesjson


def tests_should_deserialize_optional_args():
    @dataclass
    class FakeDataclass:
        test: str
        test_default: Optional[int] = None

    dataclass_ = asdataclass(
        {'test': 'test', 'test_default': '1'}, FakeDataclass
    )

    assert dataclass_.test == 'test'
    assert dataclass_.test_default == 1


def tests_should_deserialize_union_args():
    @dataclass
    class FakeDataclass:
        test_union: Union[int, str]

    dataclass_ = asdataclass({'test_union': b'1'}, FakeDataclass)

    assert dataclass_.test_union == 1


def tests_should_deserialize_bytes_to_string_on_union():
    @dataclass
    class FakeDataclass:
        test_union: str

    dataclass_ = asdataclass({'test_union': b'test'}, FakeDataclass)

    assert dataclass_.test_union == 'test'


def tests_should_deserialize_nested_jsondict():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fake: FakeDataclass

    dataclass_ = asdataclass({'fake': {'test': b'test'}}, FakeDataclass2)

    assert isinstance(dataclass_.fake, FakeDataclass)
    assert dataclass_.fake.test == 'test'


def tests_should_skip_field_deserialization():
    @dataclassesjson
    @dataclass
    class FakeDataclass:
        test: int

    dataclass_ = asdataclass({'test': '1'}, FakeDataclass)

    json = asjson(dataclass_, decoder=None)

    assert json == b'{{"test":"1"}}'
