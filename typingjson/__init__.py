"""Interoperates @dataclass with json objects"""

from typingjson.base import typingjson
from typingjson.dataclasses import asdataclass
from typingjson.schema import integer, string
from typingjson.serializers import dataclass_asjson, typed_dict_asjson
from typingjson.typed_dict import as_typed_dict


__version__ = '0.3.1'


__all__ = [
    typingjson.__name__,
    string.__name__,
    integer.__name__,
    asdataclass.__name__,
    as_typed_dict.__name__,
    dataclass_asjson.__name__,
    typed_dict_asjson.__name__,
]
