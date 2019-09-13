# dataclassesjson

<p align="center" style="margin: 3em">
  <a href="https://github.com/dutradda/dataclassesjson">
    <img src="dataclassesjson.svg" alt="dataclassesjson" width="300"/>
  </a>
</p>

<p align="center">
    <em>Interoperates <b>@dataclass</b> with <b>json objects</b></em>
</p>

---

**Documentation**: <a href="https://dutradda.github.io/dataclassesjson" target="_blank">https://dutradda.github.io/dataclassesjson</a>

**Source Code**: <a href="https://github.com/dutradda/dataclassesjson" target="_blank">https://github.com/dutradda/dataclassesjson</a>

---


## Key Features

- Full compatibility with all functions of [dataclasses](https://docs.python.org/3/library/dataclasses.html) module
- Optional input typecasting
- Direct json serialization with [orjson](https://github.com/ijl/orjson) (don't convert to dict before serialization)
- Supports custom serialization


## Requirements

 - Python 3.7+
 - [orjson](https://github.com/ijl/orjson) for json serialization


## Instalation
```
$ pip install dataclassesjson[orjson]
```


## Basic example

```python
from dataclasses import dataclass

from dataclassesjson import asdataclass, asjson


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

```

```
'{"name":"John","age":40,"music":{"name":"Imagine"}}'

```


## Example for disable typecasting

```python
from dataclassesjson import asdict, dataclass


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


person = Person(b'John', age='40', music=dict(name=b'Imagine'))

# if we use the 'asjson' function will raise error for invalid bytes type
print(asdict(person))

```

```
{
    'name':b'John',
    'age':'40',
    'music':{
        'name':b'Imagine'
    }
}

```


## Example for choose fields to typecasting

```python
from dataclassesjson import asjson, dataclass


@dataclass
class Music:
    name: str


@dataclass
class Person:
    __cast_input__ = ('name',)
    name: str
    age: int
    music: Music


person = Person(b'John', age='40', music=dict(name='Imagine'))

print(asjson(person))

```

```
'{"name":"John","age":"40","music":{"name":"Imagine"}}'

```


## Example for omit output fields

```python
from dataclassesjson import asjson, dataclass


@dataclass
class Music:
    name: str


@dataclass
class Person:
    __omit_output__ = ('music',)
    name: str
    age: int
    music: Music


person = Person('John', age=40, music=dict(name='Imagine'))

print(person)
print(asjson(person))

```

```
Person(
    'John',
    age=40,
    music=Music(name='Imagine')
)

'{"name":"John","age":40}'

```
