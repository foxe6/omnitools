import chardet
from ..xtypes import *
from .utf8 import *
from .b64 import *


__ALL__ = ["charenc"]


def charenc(b: str_or_bytes) -> str:
    if isinstance(b, str):
        b = b64d_or_utf8e(b)
    return chardet.detect(b)["encoding"]


