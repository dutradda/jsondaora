from dataclasses import asdict

from dataclassjson import dataclass


@dataclass
class Music:
    __cast_fields__ = None
    name: str


@dataclass
class Person:
    __cast_fields__ = None
    name: str
    age: int
    music: Music


person = Person(
    b'John',
    age='40',
    music=dict(name=b'Imagine')
)

# if we use the 'asjson' function will raise error for invalid bytes type
print(asdict(person))
