# dataclassjson

<p align="center" style="margin: 3em">
  <a href="https://github.com/dutradda/dataclassjson">
    <img src="dataclassjson.svg" alt="dataclassjson" width="300"/>
  </a>
</p>

<p align="center">
    <em>Interoperates <b>@dataclass</b> with <b>json objects</b></em>
</p>

---

**Documentation**: <a href="https://dutradda.github.io/dataclassjson" target="_blank">https://dutradda.github.io/dataclassjson</a>

**Source Code**: <a href="https://github.com/dutradda/dataclassjson" target="_blank">https://github.com/dutradda/dataclassjson</a>

---


## Key Features

- Full compatibility with all functions of [dataclasses]() module
- Optional input typecasting
- Direct json serialization with [orjson]() (don't convert to dict before serialization)
- Supports custom serialization


## Requirements

 - Python 3.7+
 - [orjson]()


## Instalation
```
$ pip install dataclassjson 
```


## Basic example

```python
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

```

```
'{"name":"John","age":40,"music":{"name":"Imagine"}}'

```


## Example for disable typecasting

```python
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

```

```
'{"name":"John","age":"40","music":{"name":"Imagine"}}'

```


## Example for skip fields to recurse

```python
from dataclassjson import asjson, dataclass


@dataclass
class Music:
    name: str


@dataclass
class Person:
    __skip_recursion__ = ('music',)
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

```

```
Person(
    'John',
    age=40,
    music=Music(name='Imagine')
)

'{"name":"John","age":40}'

```
