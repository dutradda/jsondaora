from dataclassjson import asjson, dataclass


@dataclass
class Music:
    name: str


@dataclass
class Person:
    __omit_output__ = ('music',)
    name: str
    age: int
    music: Music


person = Person(
    'John',
    age=40,
    music=dict(name='Imagine')
)

print(person)
print(asjson(person))
