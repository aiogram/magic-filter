from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, TypeVar

from ..attribute import Attribute
from .bases import BaseOperation

if TYPE_CHECKING:
    from .. import MagicFilter

T = TypeVar("T")
LeftOperand = TypeVar("LeftOperand")
RightOperand = TypeVar("RightOperand")


class SimpleOperation(BaseOperation, ABC):
    def __init__(self, value: Any, magic: MagicFilter) -> None:
        super().__init__(value=value)
        self.magic = magic

    @property
    def chain(self) -> List[Attribute]:
        return self.magic.chain

    def run(self, obj: Any) -> bool:
        value = self.magic.resolve_attribute(obj)
        return self.resolve(value)

    @abstractmethod
    def resolve(self, value: Any) -> bool:
        pass
