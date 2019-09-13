# type: ignore

import json
from dataclasses import _MISSING_TYPE
from typing import Optional, Union

import pytest

from dataclassjson import dataclass, asjson


class TestDataClass:
    @pytest.fixture
    def FakeDataclass(self):
        @dataclass
        class FakeDataclass:
            test: str
            test_default: Optional[int] = None

        return FakeDataclass


    def test_should_inherit_from_dataclass(self, FakeDataclass):
        assert sorted(FakeDataclass.__dataclass_fields__.keys()) == [
            'test',
            'test_default',
        ]
        assert FakeDataclass.__dataclass_fields__['test'].type == str
        assert isinstance(
            FakeDataclass.__dataclass_fields__['test'].default, _MISSING_TYPE
        )
        assert (
            FakeDataclass.__dataclass_fields__['test_default'].type
            == Union[int, None]
        )
        assert (
            FakeDataclass.__dataclass_fields__['test_default'].default == None
        )

    def tests_should_typecasting_optional_args(self, FakeDataclass):
        dataclass = FakeDataclass('test', '1')

        assert dataclass.test == 'test'
        assert dataclass.test_default == 1        

    def tests_should_typecasting_union_args(self):
        @dataclass
        class FakeDataclass:
            test_union: Union[int, str]

        dataclass_ = FakeDataclass(b'1')

        assert dataclass_.test_union == 1

    def tests_should_typecasting_bytes_to_string(self):
        @dataclass
        class FakeDataclass:
            test_union: str

        dataclass_ = FakeDataclass(b'test')

        assert dataclass_.test_union == 'test'

    def tests_should_serialize_with_default_json(self):
        @dataclass
        class FakeDataclass:
            test_union: str

        dataclass_ = FakeDataclass(b'test')

        json = asjson(dataclass_, decoder=None)

        assert json == b'{"test_union":"test"}'
