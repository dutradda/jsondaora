# type: ignore

from dataclasses import dataclass

from typingjson import asdataclass, dataclass_asjson, typingjson


def tests_should_serialize_string_with_orjson():
    @typingjson
    @dataclass
    class FakeDataclass:
        test_union: str

    dataclass_ = asdataclass({'test_union': b'test'}, FakeDataclass)

    json = dataclass_asjson(dataclass_)

    assert json == b'{"test_union":"test"}'


def tests_should_serialize_nested_dataclasses_with_orjson():
    @typingjson
    @dataclass
    class FakeDataclass:
        test: int

    @typingjson
    @dataclass
    class FakeDataclass2:
        fake: FakeDataclass

    dataclass_ = asdataclass({'fake': {'test': b'1'}}, FakeDataclass2)

    json = dataclass_asjson(dataclass_)

    assert json == b'{"fake":{"test":1}}'


def tests_should_choose_fields_to_serialize():
    @typingjson(serialize_fields=('test2',))
    @dataclass
    class FakeDataclass:
        test: int
        test2: str

    dataclass_ = asdataclass({'test': 1, 'test2': 2}, FakeDataclass)

    json = dataclass_asjson(dataclass_)

    assert json == b'{"test2":"2"}'
    assert dataclass_.test == 1
