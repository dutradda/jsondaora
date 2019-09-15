"""Interoperates @dataclass with json objects"""

from dataclassesjson.asdataclass import asdataclass
from dataclassesjson.asdict import asdict
from dataclassesjson.asjson import asjson
from dataclassesjson.dataclassjson import dataclassjson


__version__ = '0.0.4'


__all__ = [
    asdataclass.__name__,
    asjson.__name__,
    asdict.__name__,
    dataclassjson.__name__,
]
