from . import operations
from .attrdict import AttrDict
from .magic import MagicFilter

__all__ = ("operations", "MagicFilter", "F", "AttrDict")

F = MagicFilter()
