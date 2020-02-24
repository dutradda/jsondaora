# type: ignore

import dataclasses
from typing import Any, Dict, List, Optional, Set, Tuple, TypedDict, Union

import pytest

from jsondaora import (
    as_typed_dict,
    as_typed_dict_field,
    jsondaora,
    typed_dict_asjson,
)
from jsondaora.exceptions import DeserializationError


def tests_should_deserialize_optional_args():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str
        test_default: Optional[int] = None

    typed_dict = as_typed_dict(
        {'test': 'test', 'test_default': '1'}, FakeTypedDict
    )

    assert typed_dict == {'test': 'test', 'test_default': 1}


def tests_should_deserialize_union_args():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_union: Union[int, str]

    typed_dict = as_typed_dict({'test_union': b'1'}, FakeTypedDict)

    assert typed_dict == {'test_union': 1}


def tests_should_deserialize_list_args():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_list: List[int]

    typed_dict = as_typed_dict({'test_list': [b'1', '2', 3]}, FakeTypedDict)

    assert typed_dict == {'test_list': [1, 2, 3]}


def tests_should_deserialize_list_args_nested():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: List[FakeTypedDict]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2
    )

    assert typed_dict == {'fakes': fakes_data, 'fakeint': 1}


def tests_should_deserialize_bytes_to_string():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_union: str

    typed_dict = as_typed_dict({'test_union': b'test'}, FakeTypedDict)

    assert typed_dict == {'test_union': 'test'}


def tests_should_deserialize_nested_jsondict():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fake: FakeTypedDict

    typed_dict = as_typed_dict({'fake': {'test': b'test'}}, FakeTypedDict2)

    assert typed_dict == {'fake': {'test': 'test'}}


def tests_should_choose_fields_to_deserialize():
    @jsondaora(deserialize_fields=('test2',))
    class FakeTypedDict(TypedDict):
        test: int
        test2: str

    typed_dict = as_typed_dict({'test': '1', 'test2': 2}, FakeTypedDict)

    assert typed_dict == {'test': '1', 'test2': '2'}


def tests_should_serialize_all_fields_with_choosen_deserialize_fields():
    @jsondaora(deserialize_fields=('test2',))
    class FakeTypedDict(TypedDict):
        test: int
        test2: str

    typed_dict = as_typed_dict({'test': '1', 'test2': 2}, FakeTypedDict)

    assert typed_dict_asjson(typed_dict, FakeTypedDict) in [
        b'{"test":"1","test2":"2"}',
        b'{"test2":"2","test":"1"}',
    ]


def tests_should_set_dataclass_fields_on_typed_dict():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: int
        test2: str

    fields = dataclasses.fields(FakeTypedDict)

    assert len(fields) == 2
    assert fields[0].type == int
    assert fields[1].type == str


def tests_should_set_dataclass_fields_on_typed_dict_with_inheritance():
    @jsondaora
    class FakeTypedDict2(TypedDict):
        test: float

    @jsondaora
    class FakeTypedDict(FakeTypedDict2):
        test2: int
        test3: str

    @jsondaora
    class Fake:
        fake: FakeTypedDict

    fake = Fake(FakeTypedDict2())

    fake_field = type(fake).__dataclass_fields__[  # type: ignore
        'fake'
    ]
    assert fake_field.type is FakeTypedDict


def tests_should_deserialize_list_args_nested_as_list():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: List[FakeTypedDict]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    typed_dict_list = as_typed_dict_field(
        [{'fakes': fakes_data, 'fakeint': '1'}], 'list', List[FakeTypedDict2]
    )

    assert typed_dict_list == [{'fakes': fakes_data, 'fakeint': 1}]


def tests_should_deserialize_tuple_args_limited():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_tuple: Tuple[int, str]

    typed_dict_tuple = as_typed_dict({'test_tuple': [b'1', 2]}, FakeTypedDict)

    assert typed_dict_tuple == {'test_tuple': (1, '2')}


def tests_should_deserialize_tuple_args_nested_limited():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: Tuple[FakeTypedDict, int]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, '1']
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2
    )

    assert typed_dict == {
        'fakes': ({'test': 'fake11'}, 1),
        'fakeint': 1,
    }


def tests_should_raise_error_when_deserializing_invalid_tuple_size():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: Tuple[FakeTypedDict, int]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, '1', None]

    with pytest.raises(DeserializationError) as exc_info:
        as_typed_dict({'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2)

    assert exc_info.value.args == (
        f'Invalid type={Tuple[FakeTypedDict, int]} for field=fakes',
    )


def tests_should_deserialize_set_args():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_set: Set[int]

    typed_dict = as_typed_dict({'test_set': [b'1', '2', 3]}, FakeTypedDict)

    assert typed_dict == {'test_set': {1, 2, 3}}


def tests_should_deserialize_set_args_nested():
    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: Set[Tuple[int, str, float]]
        fakeint: int

    fakes_data = [[1, 2, 3]]
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2
    )

    assert typed_dict == {'fakes': {(1, '2', 3.0)}, 'fakeint': 1}


def tests_should_deserialize_dict_args():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_dict: Dict[int, str]

    typed_dict = as_typed_dict(
        {'test_dict': {b'1': b'1', '2': '2', 3: 3}}, FakeTypedDict
    )

    assert typed_dict == {'test_dict': {1: '1', 2: '2', 3: '3'}}


def tests_should_deserialize_dict_args_nested():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: Dict[int, List[FakeTypedDict]]
        fakeint: int

    fakes_data = {
        b'1': [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    }
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2
    )

    assert typed_dict == FakeTypedDict2(
        {
            'fakes': {
                1: [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
            },
            'fakeint': 1,
        },
    )


def tests_should_deserialize_any():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test_any: Any

    typed_dict1 = as_typed_dict({'test_any': 0.1}, FakeTypedDict)
    any_object = object()
    typed_dict2 = as_typed_dict({'test_any': any_object}, FakeTypedDict)

    assert typed_dict1 == {'test_any': 0.1}
    assert typed_dict2 == {'test_any': any_object}


def tests_should_deserialize_any_nested():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: Set[Any]
        fakeint: int

    any_object = object()
    fakes_data = [any_object, 0.1]
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeTypedDict2
    )

    assert typed_dict == {
        'fakes': {any_object, 0.1},
        'fakeint': 1,
    }
