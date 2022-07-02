import pkg_resources

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

__version__ = pkg_resources.get_distribution(__name__).version

F = MagicFilter()
