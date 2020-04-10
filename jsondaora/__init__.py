"""Interoperates @dataclass with json objects"""

from jsondaora.dataclasses import asdataclass
from jsondaora.decorator import jsondaora
from jsondaora.schema import IntegerField, StringField, integer, string
from jsondaora.serializers import dataclass_asjson, typed_dict_asjson
from jsondaora.typed_dict import as_typed_dict, as_typed_dict_field


__version__ = '0.11.1'


__all__ = [
    'jsondaora',
    'StringField',
    'IntegerField',
    'asdataclass',
    'as_typed_dict',
    'as_typed_dict_field',
    'dataclass_asjson',
    'typed_dict_asjson',
    'integer',
    'string',
]
