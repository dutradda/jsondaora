from dataclassjson import asdict, dataclass


@dataclass
class Music:
    __cast_input__ = None
    name: str


@dataclass
class Person:
    __cast_input__ = None
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
