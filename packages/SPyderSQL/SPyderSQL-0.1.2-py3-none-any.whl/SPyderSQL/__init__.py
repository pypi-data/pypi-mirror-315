from .__meta__ import __version__, __author__, __email__, __description__, __url__

from .client import SQLite
from .client.SQLite import TypesSQLite
from .logger import Logger


logger = Logger(__name__).get_logger()
#
__all__ = (
    '__version__',
    '__author__',
    '__email__',
    '__description__',
    '__url__',
    'SQLite',
    'TypesSQLite',
    'logger'
)