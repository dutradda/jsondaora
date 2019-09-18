"""Interoperates @dataclass with json objects"""

from dataclassesjson.asdataclass import asdataclass
from dataclassesjson.asdict import asdict
from dataclassesjson.asjson import asjson
from dataclassesjson.dataclassjson import dataclassjson
from dataclassesjson.schema import integer, string


__version__ = '0.2.0'


__all__ = [
    asdataclass.__name__,
    asjson.__name__,
    asdict.__name__,
    dataclassjson.__name__,
    string.__name__,
    integer.__name__,
]
