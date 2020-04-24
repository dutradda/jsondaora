# jsondaora

<p align="center" style="margin: 3em">
  <a href="https://github.com/dutradda/jsondaora">
    <img src="https://dutradda.github.io/jsondaora/jsondaora.svg" alt="jsondaora" width="300"/>
  </a>
</p>

<p align="center">
    <em>Interoperates <b>dataclasses</b> and <b>TypedDict</b> annotations with <b>json objects for python</b></em>
</p>

---

**Documentation**: <a href="https://dutradda.github.io/jsondaora" target="_blank">https://dutradda.github.io/jsondaora</a>

**Source Code**: <a href="https://github.com/dutradda/jsondaora" target="_blank">https://github.com/dutradda/jsondaora</a>

---


## Key Features

- Full compatibility with [dataclasses](https://docs.python.org/3/library/dataclasses.html) module and [TypedDict](https://www.python.org/dev/peps/pep-0589/) annotation
- Deserialize values from dict
- Deserialize values from bytes*
- Deserialization/serialization of chosen fields
- Deserialize the following standard types: Dict, List, Tuple, Set, Union and Any
- Dict serialization
- Direct json serialization with [orjson](https://github.com/ijl/orjson) (don't convert to dict recursively before serialization)
- Optional validation according with the [json-schema](https://json-schema.org/) specification*

*\* feature in development.*


## Requirements

 - Python 3.8+
 - [orjson](https://github.com/ijl/orjson) for json serialization


## Installation
```
$ pip install jsondaora
```


## Basic example

```python
from typing import List, TypedDict

from jsondaora import (
    as_typed_dict,
    asdataclass,
    dataclass_asjson,
    jsondaora,
    typed_dict_asjson,
)


@jsondaora
class Person:
    name: str
    age: int

    class Music:
        name: str

    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print('dataclass:')
print(person)
print(dataclass_asjson(person))
print()


# TypedDict


@jsondaora
class MusicT(TypedDict):
    name: str


@jsondaora
class PersonT(TypedDict):
    name: str
    age: int

    musics: List[MusicT]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = as_typed_dict(jsondict, PersonT)

print('TypedDict:')
print(person)
print(typed_dict_asjson(person, Person))

```

```
dataclass:
Person(name='John', age=40, musics=[Person.Music(name='Imagine')])
b'{"name":"John","age":40,"musics":[{"name":"Imagine"}]}'

TypedDict:
{'name': 'John', 'age': 40, 'musics': [{'name': 'Imagine'}]}
b'{"name":"John","age":40,"musics":[{"name":"Imagine"}]}'

```


## Example for choose fields to deserialize

```python
from typing import List, TypedDict

from jsondaora import (
    as_typed_dict,
    asdataclass,
    dataclass_asjson,
    jsondaora,
    typed_dict_asjson,
)


@jsondaora(deserialize_fields=('name'))
class Person:
    name: str
    age: int

    class Music:
        name: str

    musics: List[Music]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = asdataclass(jsondict, Person)

print('dataclass:')
print(person)
print(dataclass_asjson(person))
print()


# TypedDict


@jsondaora
class MusicT(TypedDict):
    name: str


@jsondaora(deserialize_fields=('name',))
class PersonT(TypedDict):
    name: str
    age: int

    musics: List[MusicT]


jsondict = dict(name=b'John', age='40', musics=[dict(name='Imagine')])
person = as_typed_dict(jsondict, PersonT)

print('TypedDict:')
print(person)
print(typed_dict_asjson(person, PersonT))

```

```
dataclass:
Person(name='John', age='40', musics=[{'name': 'Imagine'}])
b'{"name":"John","age":"40","musics":[{"name":"Imagine"}]}'

TypedDict:
{'name': 'John', 'musics': [{'name': 'Imagine'}], 'age': '40'}
b'{"name":"John","musics":[{"name":"Imagine"}],"age":"40"}'

```


## Example for choose fields to serialize

```python
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

```

```
dataclass:
Person(name='John', age=40, musics=[Person.Music(name='Imagine')])
b'{"age":40,"name":"John"}'

TypedDict:
{'name': 'John', 'age': 40, 'musics': [{'name': 'Imagine'}]}
b'{"age":40}'

```
