from typing import TYPE_CHECKING, Any, Callable

from ..helper import resolve_if_needed
from .base import BaseOperation

if TYPE_CHECKING:  # pragma: no cover
    from magic_filter.magic import MagicFilter


class CombinationOperation(BaseOperation):
    __slots__ = (
        "right",
        "combinator",
    )

    def __init__(self, right: Any, combinator: Callable[[Any, Any], bool]) -> None:
        self.right = right
        self.combinator = combinator

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return self.combinator(value, resolve_if_needed(self.right, initial_value=initial_value))

    @classmethod
    def and_op(cls, right: "MagicFilter") -> "CombinationOperation":
        return cls(right=right, combinator=and_op)

    @classmethod
    def or_op(cls, right: "MagicFilter") -> "CombinationOperation":
        return cls(right=right, combinator=or_op)


class RCombinationOperation(BaseOperation):
    __slots__ = (
        "left",
        "combinator",
    )

    def __init__(self, left: Any, combinator: Callable[[Any, Any], bool]) -> None:
        self.left = left
        self.combinator = combinator

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return self.combinator(resolve_if_needed(self.left, initial_value), value)


def and_op(a: Any, b: Any) -> Any:
    return a and b


def or_op(a: Any, b: Any) -> Any:
    return a or b
