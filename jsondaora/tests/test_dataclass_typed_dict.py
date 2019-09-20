# type: ignore

from typing import List, TypedDict

from jsondaora import as_typed_dict, asdataclass, jsondaora


def tests_should_deserialize_nested_dataclass_typed_dict():
    @jsondaora
    class FakeTypedDict(TypedDict):
        test: str

    @jsondaora
    class FakeDataclass:
        fake: FakeTypedDict

    dataclass = asdataclass({'fake': {'test': b'test'}}, FakeDataclass)

    assert dataclass == FakeDataclass(fake={'test': 'test'})


def tests_should_deserialize_nested_typed_dict_dataclass():
    @jsondaora
    class FakeDataclass:
        test: str

    @jsondaora
    class FakeTypedDict(TypedDict):
        fake: FakeDataclass

    typed_dict = as_typed_dict({'fake': {'test': b'test'}}, FakeTypedDict)

    assert typed_dict == {'fake': FakeDataclass(test='test')}


def tests_should_deserialize_list_args_nested_dataclass_typed_dict():
    @jsondaora
    class FakeTypedDict(TypedDict):
        fakeint: int

    @jsondaora
    class FakeDataclass:
        fakes: List[FakeTypedDict]
        fakefloat: float

    fakes_data = [{'fakeint': '1'}, {'fakeint': '2'}, {'fakeint': '3'}]
    dataclass = asdataclass(
        {'fakes': fakes_data, 'fakefloat': '0.1'}, FakeDataclass
    )

    assert dataclass == FakeDataclass(
        fakefloat=0.1, fakes=[{'fakeint': 1}, {'fakeint': 2}, {'fakeint': 3}]
    )


def tests_should_deserialize_list_args_nested_typed_dict_dataclass():
    @jsondaora
    class FakeDataclass:
        fakeint: int

    @jsondaora
    class FakeTypedDict(TypedDict):
        fakes: List[FakeDataclass]
        fakefloat: float

    fakes_data = [{'fakeint': '1'}, {'fakeint': '2'}, {'fakeint': '3'}]
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakefloat': '0.1'}, FakeTypedDict
    )

    assert typed_dict == {
        'fakes': [FakeDataclass(1), FakeDataclass(2), FakeDataclass(3)],
        'fakefloat': 0.1,
    }


def tests_should_deserialize_list_args_deep_nested_typed_dict_dataclass():
    @jsondaora
    class FakeDataclass2:
        fakeint: int

    @jsondaora
    class FakeTypedDict2(TypedDict):
        fakes: List[FakeDataclass2]
        fakefloat: float

    @jsondaora
    class FakeDataclass:
        fakeint: int
        fake: FakeTypedDict2

    @jsondaora
    class FakeTypedDict(TypedDict):
        fakes: List[FakeDataclass]
        fakefloat: float

    fakes_data = [
        {
            'fakeint': '1',
            'fake': {'fakefloat': '0.2', 'fakes': [{'fakeint': '-1'}]},
        },
        {
            'fakeint': '2',
            'fake': {'fakefloat': '0.3', 'fakes': [{'fakeint': '-2'}]},
        },
        {
            'fakeint': '3',
            'fake': {'fakefloat': '0.4', 'fakes': [{'fakeint': '0'}]},
        },
    ]
    typed_dict = as_typed_dict(
        {'fakes': fakes_data, 'fakefloat': '0.1'}, FakeTypedDict
    )

    assert typed_dict == {
        'fakes': [
            FakeDataclass(
                fakeint=1,
                fake={'fakefloat': 0.2, 'fakes': [FakeDataclass2(fakeint=-1)]},
            ),
            FakeDataclass(
                fakeint=2,
                fake={'fakefloat': 0.3, 'fakes': [FakeDataclass2(fakeint=-2)]},
            ),
            FakeDataclass(
                fakeint=3,
                fake={'fakefloat': 0.4, 'fakes': [FakeDataclass2(fakeint=0)]},
            ),
        ],
        'fakefloat': 0.1,
    }
