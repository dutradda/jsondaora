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
{!./src/index/index_00_basic.py!}
```

```
{!./src/index/index_00_basic.result!}
```


## Example for disable typecasting

```python
{!./src/index/index_01_disable_typecasting.py!}
```

```
{!./src/index/index_01_disable_typecasting.result!}
```


## Example for choose fields to typecasting

```python
{!./src/index/index_02_typecasting_fields.py!}
```

```
{!./src/index/index_02_typecasting_fields.result!}
```


## Example for skip fields to recurse

```python
{!./src/index/index_03_skip_recursive_fields.py!}
```

```
{!./src/index/index_03_skip_recursive_fields.result!}
```
