"""Interoperates @dataclass with json objects"""

from dataclassesjson.asdataclass import asdataclass
from dataclassesjson.asdict import asdict
from dataclassesjson.asjson import asjson, dataclassesjson


__version__ = '0.0.1'


__all__ = [
    asdataclass.__name__,
    asjson.__name__,
    asdict.__name__,
    dataclassesjson.__name__,
]
