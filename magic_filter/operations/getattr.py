from abc import ABC
from typing import Any

from .base import BaseOperation


class GetAttributeOperation(BaseOperation, ABC):
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def resolve(self, value: Any, initial_value: Any) -> Any:
        try:
            return getattr(value, self.name)
        except AttributeError:
            return None
