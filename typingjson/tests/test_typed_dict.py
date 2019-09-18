# type: ignore

from typing import List, Optional, TypedDict, Union

from typingjson import as_typed_dict, asjson, typingjson


def tests_should_deserialize_optional_args():
    @typingjson
    class FakeTypedDict(TypedDict):
        test: str
        test_default: Optional[int] = None

    typed_dict = as_typed_dict(
        {'test': 'test', 'test_default': '1'}, FakeTypedDict
    )

    assert typed_dict == {'test': 'test', 'test_default': 1}


def tests_should_deserialize_union_args():
    @typingjson
    class FakeTypedDict(TypedDict):
        test_union: Union[int, str]

    typed_dict = as_typed_dict({'test_union': b'1'}, FakeTypedDict)

    assert typed_dict == {'test_union': 1}


def tests_should_deserialize_list_args():
    @typingjson
    class FakeTypedDict(TypedDict):
        test_list: List[int]

    typed_dict = as_typed_dict({'test_list': [b'1', '2', 3]}, FakeTypedDict)

    assert typed_dict == {'test_list': [1, 2, 3]}


def tests_should_deserialize_list_args_nested():
    @typingjson
    class FakeTypedDict(TypedDict):
        test: str

    @typingjson
    class FakeTypedDict2(TypedDict):
        fakes: List[FakeTypedDict]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2
    )

    assert typed_dict == {'fakes': fakes_data, 'fakeint': 1}


def tests_should_deserialize_bytes_to_string():
    @typingjson
    class FakeTypedDict(TypedDict):
        test_union: str

    typed_dict = as_typed_dict({'test_union': b'test'}, FakeTypedDict)

    assert typed_dict == {'test_union': 'test'}


def tests_should_deserialize_nested_jsondict():
    @typingjson
    class FakeTypedDict(TypedDict):
        test: str

    @typingjson
    class FakeTypedDict2(TypedDict):
        fake: FakeTypedDict

    typed_dict = as_typed_dict({'fake': {'test': b'test'}}, FakeTypedDict2)

    assert typed_dict == {'fake': {'test': 'test'}}


def tests_should_choose_fields_to_deserialize():
    @typingjson(deserialize_fields=('test2',))
    class FakeTypedDict(TypedDict):
        test: int
        test2: str

    typed_dict = as_typed_dict({'test': '1', 'test2': 2}, FakeTypedDict)

    assert typed_dict == {'test': '1', 'test2': '2'}


def tests_should_serialize_all_fields_with_choosen_deserialize_fields():
    @typingjson(deserialize_fields=('test2',))
    class FakeTypedDict(TypedDict):
        test: int
        test2: str

    typed_dict = as_typed_dict({'test': '1', 'test2': 2}, FakeTypedDict)

    assert asjson(typed_dict) in [
        b'{"test":"1","test2":"2"}',
        b'{"test2":"2","test":"1"}',
    ]