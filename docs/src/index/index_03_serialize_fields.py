from dataclasses import dataclass
from typing import List

from typingjson import asdataclass, asjson, typingjson


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

print(person)
print(asjson(person))
