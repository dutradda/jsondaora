"""Interoperates @dataclass with json objects"""

from jsondaora.base import jsondaora
from jsondaora.dataclasses import asdataclass
from jsondaora.schema import integer, string
from jsondaora.serializers import dataclass_asjson, typed_dict_asjson
from jsondaora.typed_dict import as_typed_dict, as_typed_dict_field


__version__ = '0.4.0'


__all__ = [
    jsondaora.__name__,
    string.__name__,
    integer.__name__,
    asdataclass.__name__,
    as_typed_dict.__name__,
    as_typed_dict_field.__name__,
    dataclass_asjson.__name__,
    typed_dict_asjson.__name__,
]
