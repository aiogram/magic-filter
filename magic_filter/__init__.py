from . import operations
from .magic import F, MagicFilter

__all__ = ["F", "MagicFilter", "operations", "compiled"]

__version__ = "0.1.1"

try:  # pragma: no cover
    import cython
except ImportError:
    compiled: bool = False
else:  # pragma: no cover
    try:
        compiled = cython.compiled
    except AttributeError:
        compiled = False
