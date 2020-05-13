from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from ..attribute import resolve_attribute
from .bases import BaseOperation

if TYPE_CHECKING:
    from .. import MagicFilter


class SimpleOperation(BaseOperation, ABC):
    def __init__(self, value: Any, magic: MagicFilter) -> None:
        super().__init__(value=value)
        self.magic = magic

    def __call__(self, obj: Any) -> bool:
        value = resolve_attribute(obj, self.magic.get_chain())
        return self.resolve(value)

    @abstractmethod
    def resolve(self, value: Any) -> bool:
        pass

    __slots__ = ("value", "magic")
