from abc import ABC, abstractmethod
from typing import Any, List

from ..attribute import Attribute, resolve_attribute
from .bases import BaseOperation


class SimpleOperation(BaseOperation, ABC):
    def __init__(self, value: Any, chain: List[Attribute]) -> None:
        super().__init__(value=value)
        self._chain = chain

    def __call__(self, obj: Any) -> bool:
        try:
            value = resolve_attribute(obj, self._chain)
        except AttributeError:
            return False
        return self.resolve(value)

    @abstractmethod
    def resolve(self, value: Any) -> bool:
        pass

    __slots__ = ("value", "magic", "_chain")
