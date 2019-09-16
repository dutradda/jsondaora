from dataclasses import dataclass
from typing import List

from dataclassesjson import asdataclass, asjson, dataclassjson


@dataclass
class Music:
    name: str


@dataclassjson(deserialize_fields=('name', 'age'))
@dataclass
class Person:
    name: str
    age: int
    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print(person)
print(asjson(person))
