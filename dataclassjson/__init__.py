"""Interoperates @dataclass with json objects"""

from dataclassjson._asjson import _asjson
from dataclassjson.dataclass import dataclass


__version__ = '0.0.1'

asjson = _asjson

__all__ = [dataclass.__name__, asjson.__name__]
