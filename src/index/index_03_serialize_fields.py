from dataclasses import dataclass
from typing import List, TypedDict

from typingjson import (
    as_typed_dict,
    asdataclass,
    dataclass_asjson,
    typed_dict_asjson,
    typingjson,
)


@dataclass
class Music:
    name: str


@typingjson(serialize_fields=('name', 'age'))
@dataclass
class Person:
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name='John', age=40, musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print('dataclass:')
print(person)
print(dataclass_asjson(person))
print()


# TypedDict


@typingjson
class Music(TypedDict):
    name: str


@typingjson(serialize_fields=('age'))
class Person(TypedDict):
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = as_typed_dict(jsondict, Person)

print('TypedDict:')
print(person)
print(typed_dict_asjson(person, Person))
