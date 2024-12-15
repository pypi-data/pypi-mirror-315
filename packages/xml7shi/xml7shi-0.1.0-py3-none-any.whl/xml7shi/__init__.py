from importlib.metadata import version

try:
    __version__ = version("xml7shi")
except:
    __version__ = "unknown"

from .xml7shi import reader, declaration

__all__ = [
    'reader',
    'declaration'
]
