from . import operations
from .attrdict import AttrDict
from .magic import MagicFilter, MagicT

__all__ = (
    "operations",
    "MagicFilter",
    "MagicT",
    "F",
    "AttrDict",
)

F = MagicFilter()
