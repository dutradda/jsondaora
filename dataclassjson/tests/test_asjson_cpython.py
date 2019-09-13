# type: ignore

from dataclasses import dataclass

from dataclassjson import asdataclass, asjson


def tests_should_serialize_string_with_cpython_json():
    @dataclass
    class FakeDataclass:
        test_union: str

    dataclass_ = asdataclass({'test_union': b'test'}, FakeDataclass)

    json = asjson(dataclass_, decoder=None)

    assert json == b'{"test_union":"test"}'


def tests_should_serialize_nested_dataclasses_with_cpython_json():
    @dataclass
    class FakeDataclass:
        test: int

    @dataclass
    class FakeDataclass2:
        fake: FakeDataclass

    dataclass_ = asdataclass({'fake': {'test': b'1'}}, FakeDataclass2)

    json = asjson(dataclass_, decoder=None)

    assert json == b'{"fake":{"test":1}}'
