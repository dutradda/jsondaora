from typing import List, TypedDict

from jsondaora import (
    as_typed_dict,
    asdataclass,
    dataclass_asjson,
    jsondaora,
    typed_dict_asjson,
)


@jsondaora(serialize_fields=('name', 'age'))
class Person:
    name: str
    age: int

    class Music:
        name: str

    musics: List[Music]


jsondict = dict(name='John', age=40, musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print('dataclass:')
print(person)
print(dataclass_asjson(person))
print()


# TypedDict


@jsondaora
class Music(TypedDict):
    name: str


@jsondaora(serialize_fields=('age',))
class PersonT(TypedDict):
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = as_typed_dict(jsondict, PersonT)

print('TypedDict:')
print(person)
print(typed_dict_asjson(person, PersonT))
