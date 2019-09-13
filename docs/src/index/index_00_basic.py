from dataclasses import dataclass

from dataclassjson import asdataclass, asjson


@dataclass
class Music:
    name: str


@dataclass
class Person:
    name: str
    age: int
    music: Music


jsondict = dict(name=b'John', age='40', music=dict(name='Imagine'))
person = asdataclass(jsondict, Person)

print(asjson(person))
