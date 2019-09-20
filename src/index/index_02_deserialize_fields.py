from dataclasses import dataclass
from typing import List, TypedDict

from jsondaora import (
    as_typed_dict,
    asdataclass,
    dataclass_asjson,
    jsondaora,
    typed_dict_asjson,
)


@dataclass
class Music:
    name: str


@jsondaora(deserialize_fields=('name'))
class Person:
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print('dataclass:')
print(person)
print(dataclass_asjson(person))
print()


# TypedDict


@jsondaora
class Music(TypedDict):
    name: str


@jsondaora(deserialize_fields=('name'))
class Person(TypedDict):
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = as_typed_dict(jsondict, Person)

print('TypedDict:')
print(person)
print(typed_dict_asjson(person, Person))
