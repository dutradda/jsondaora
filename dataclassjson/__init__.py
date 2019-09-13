"""Interoperates @dataclass with json objects"""

from dataclassjson.asdataclass import asdataclass
from dataclassjson.asdict import asdict
from dataclassjson.asjson import asjson, dataclassjson


__version__ = '0.0.1'


__all__ = [
    asdataclass.__name__,
    asjson.__name__,
    asdict.__name__,
    dataclassjson.__name__,
]
