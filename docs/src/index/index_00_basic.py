from dataclassjson import asjson, dataclass


@dataclass
class Music:
    name: str


@dataclass
class Person:
    name: str
    age: int
    music: Music


person = Person(
    b'John',
    age='40',
    music=dict(name='Imagine')
)

print(asjson(person))
