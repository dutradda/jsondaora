"""Interoperates @dataclass with json objects"""

from jsondaora.base import jsondaora
from jsondaora.dataclasses import asdataclass
from jsondaora.schema import integer, string
from jsondaora.serializers import dataclass_asjson, typed_dict_asjson
from jsondaora.typed_dict import as_typed_dict, as_typed_dict_field


__version__ = '0.8.1'


__all__ = [
    'jsondaora',
    'string',
    'integer',
    'asdataclass',
    'as_typed_dict',
    'as_typed_dict_field',
    'dataclass_asjson',
    'typed_dict_asjson',
]
