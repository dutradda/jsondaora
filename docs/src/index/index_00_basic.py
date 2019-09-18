from dataclasses import dataclass
from typing import List

from typingjson import asdataclass, asjson, typingjson


@dataclass
class Music:
    name: str


@typingjson
@dataclass
class Person:
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print(person)
print(asjson(person))
