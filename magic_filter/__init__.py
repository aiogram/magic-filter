from . import operations
from .attrdict import AttrDict
from .magic import MagicFilter, MagicT

__all__ = (
    "__version__",
    "operations",
    "MagicFilter",
    "MagicT",
    "F",
    "AttrDict",
)

__version__ = "1"

F = MagicFilter()
