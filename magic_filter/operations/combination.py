from typing import TYPE_CHECKING, Any, Callable

from .base import BaseOperation

if TYPE_CHECKING:  # pragma: no cover
    from magic_filter.magic import MagicFilter


class CombinationOperation(BaseOperation):
    __slots__ = (
        "right",
        "combinator",
    )

    def __init__(self, right: "MagicFilter", combinator: Callable[[Any, Any], bool]) -> None:
        self.right = right
        self.combinator = combinator

    def resolve(self, value: Any, initial_value: Any) -> Any:
        right = self.right.resolve(initial_value)
        return self.combinator(value, right)

    @classmethod
    def and_op(cls, right: "MagicFilter") -> "CombinationOperation":
        return cls(right=right, combinator=and_op)

    @classmethod
    def or_op(cls, right: "MagicFilter") -> "CombinationOperation":
        return cls(right=right, combinator=or_op)


def and_op(a: Any, b: Any) -> Any:
    return a and b


def or_op(a: Any, b: Any) -> Any:
    return a or b
