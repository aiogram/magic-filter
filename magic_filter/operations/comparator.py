from typing import Any, Callable

from .base import BaseOperation


class ComparatorOperation(BaseOperation):
    __slots__ = (
        "right",
        "comparator",
    )

    def __init__(self, right: Any, comparator: Callable[[Any, Any], bool]) -> None:
        self.right = right
        self.comparator = comparator

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return self.comparator(value, self.right)
