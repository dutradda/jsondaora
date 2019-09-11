from dataclassjson import asjson, dataclass


@dataclass
class Music:
    name: str


@dataclass
class Person:
    __cast_fields__ = ('name',)
    name: str
    age: int
    music: Music


person = Person(
    b'John',
    age='40',
    music=dict(name='Imagine')
)

print(asjson(person))
