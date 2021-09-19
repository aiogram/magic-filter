from functools import partial
from typing import Any, Callable

from .base import BaseOperation


class FunctionOperation(BaseOperation):
    __slots__ = ("function",)

    def __init__(self, function: Callable[[Any], Any]) -> None:
        self.function = function

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return self.function(value)

    @classmethod
    def in_op(cls, a: Any) -> "FunctionOperation":
        return cls(function=partial(in_op, a))

    @classmethod
    def contains_op(cls, a: Any) -> "FunctionOperation":
        return cls(function=partial(contains_op, a))


class ImportantFunctionOperation(FunctionOperation):
    important = True


def in_op(a: Any, b: Any) -> bool:
    try:
        return b in a
    except TypeError:
        return False


def contains_op(a: Any, b: Any) -> bool:
    try:
        return a in b
    except TypeError:
        return False
