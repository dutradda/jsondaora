# type: ignore

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pytest

from jsondaora import asdataclass, dataclass_asjson, jsondaora
from jsondaora.exceptions import DeserializationError


def tests_should_deserialize_optional_args():
    @dataclass
    class FakeDataclass:
        test: str
        test_default: Optional[int] = None

    dataclass_ = asdataclass(
        {'test': 'test', 'test_default': '1'}, FakeDataclass
    )

    assert dataclass_ == FakeDataclass('test', 1)


def tests_should_deserialize_union_args():
    @dataclass
    class FakeDataclass:
        test_union: Union[int, str]

    dataclass_ = asdataclass({'test_union': b'1'}, FakeDataclass)

    assert dataclass_ == FakeDataclass(1)


def tests_should_deserialize_list_args():
    @dataclass
    class FakeDataclass:
        test_list: List[int]

    dataclass_ = asdataclass({'test_list': [b'1', '2', 3]}, FakeDataclass)

    assert dataclass_ == FakeDataclass([1, 2, 3])


def tests_should_deserialize_list_args_nested():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: List[FakeDataclass]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    dataclass_ = asdataclass(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2
    )

    assert dataclass_ == FakeDataclass2(
        [
            FakeDataclass('fake11'),
            FakeDataclass('fake12'),
            FakeDataclass('fake13'),
        ],
        1,
    )


def tests_should_deserialize_tuple_args():
    @dataclass
    class FakeDataclass:
        test_tuple: Tuple[int, ...]

    dataclass_ = asdataclass({'test_tuple': [b'1', '2', 3]}, FakeDataclass)

    assert dataclass_ == FakeDataclass((1, 2, 3))


def tests_should_deserialize_tuple_args_nested():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: Tuple[FakeDataclass, ...]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    dataclass_ = asdataclass(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2
    )

    assert dataclass_ == FakeDataclass2(
        (
            FakeDataclass('fake11'),
            FakeDataclass('fake12'),
            FakeDataclass('fake13'),
        ),
        1,
    )


def tests_should_deserialize_tuple_args_limited():
    @dataclass
    class FakeDataclass:
        test_tuple: Tuple[int, str]

    dataclass_ = asdataclass({'test_tuple': [b'1', 2]}, FakeDataclass)

    assert dataclass_ == FakeDataclass((1, '2'))


def tests_should_deserialize_tuple_args_nested_limited():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: Tuple[FakeDataclass, int]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, '1']
    dataclass_ = asdataclass(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2
    )

    assert dataclass_ == FakeDataclass2((FakeDataclass('fake11'), 1), 1,)


def tests_should_raise_error_when_deserializing_invalid_tuple_size():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: Tuple[FakeDataclass, int]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, '1', None]

    with pytest.raises(DeserializationError) as exc_info:
        asdataclass({'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2)

    assert exc_info.value.args == (
        f'Invalid type={Tuple[FakeDataclass, int]} for field=fakes',
    )


def tests_should_deserialize_set_args():
    @dataclass
    class FakeDataclass:
        test_set: Set[int]

    dataclass_ = asdataclass({'test_set': [b'1', '2', 3]}, FakeDataclass)

    assert dataclass_ == FakeDataclass({1, 2, 3})


def tests_should_deserialize_set_args_nested():
    @dataclass(unsafe_hash=True)
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: Set[FakeDataclass]
        fakeint: int

    fakes_data = [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    dataclass_ = asdataclass(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2
    )

    assert dataclass_ == FakeDataclass2(
        {
            FakeDataclass('fake11'),
            FakeDataclass('fake12'),
            FakeDataclass('fake13'),
        },
        1,
    )


def tests_should_deserialize_dict_args():
    @dataclass
    class FakeDataclass:
        test_dict: Dict[int, str]

    dataclass_ = asdataclass(
        {'test_dict': {b'1': b'1', '2': '2', 3: 3}}, FakeDataclass
    )

    assert dataclass_ == FakeDataclass({1: '1', 2: '2', 3: '3'})


def tests_should_deserialize_dict_args_nested():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: Dict[int, List[FakeDataclass]]
        fakeint: int

    fakes_data = {
        b'1': [{'test': 'fake11'}, {'test': 'fake12'}, {'test': 'fake13'}]
    }
    dataclass_ = asdataclass(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2
    )

    assert dataclass_ == FakeDataclass2(
        {
            1: [
                FakeDataclass('fake11'),
                FakeDataclass('fake12'),
                FakeDataclass('fake13'),
            ]
        },
        1,
    )


def tests_should_deserialize_any():
    @dataclass
    class FakeDataclass:
        test_any: Any

    dataclass1 = asdataclass({'test_any': 0.1}, FakeDataclass)
    any_object = object()
    dataclass2 = asdataclass({'test_any': any_object}, FakeDataclass)

    assert dataclass1 == FakeDataclass(0.1)
    assert dataclass2 == FakeDataclass(any_object)


def tests_should_deserialize_any_nested():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fakes: Set[Any]
        fakeint: int

    any_object = object()
    fakes_data = [any_object, 0.1]
    dataclass_ = asdataclass(
        {'fakes': fakes_data, 'fakeint': '1'}, FakeDataclass2
    )

    assert dataclass_ == FakeDataclass2({any_object, 0.1}, 1,)


def tests_should_deserialize_bytes_to_string():
    @dataclass
    class FakeDataclass:
        test_union: str

    dataclass_ = asdataclass({'test_union': b'test'}, FakeDataclass)

    assert dataclass_ == FakeDataclass('test')


def tests_should_deserialize_nested_jsondict():
    @dataclass
    class FakeDataclass:
        test: str

    @dataclass
    class FakeDataclass2:
        fake: FakeDataclass

    dataclass_ = asdataclass({'fake': {'test': b'test'}}, FakeDataclass2)

    assert dataclass_ == FakeDataclass2(FakeDataclass('test'))


def tests_should_choose_fields_to_deserialize():
    @jsondaora(deserialize_fields=('test2',))
    @dataclass
    class FakeDataclass:
        test: int
        test2: str

    dataclass_ = asdataclass({'test': '1', 'test2': 2}, FakeDataclass)

    assert dataclass_ == FakeDataclass('1', '2')


def tests_should_serialize_all_fields_with_choosen_deserialize_fields():
    @jsondaora(deserialize_fields=('test2',))
    @dataclass
    class FakeDataclass:
        test: int
        test2: str

    dataclass_ = asdataclass({'test': '1', 'test2': 2}, FakeDataclass)

    assert dataclass_asjson(dataclass_) == b'{"test":"1","test2":"2"}'
