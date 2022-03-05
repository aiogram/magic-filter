from typing import Any, Callable

from ..exceptions import RejectOperations
from ..helper import resolve_if_needed
from .base import BaseOperation


class FunctionOperation(BaseOperation):
    __slots__ = ("function", "args")

    def __init__(self, function: Callable[..., Any], *args: Any) -> None:
        self.function = function
        self.args = args

    def resolve(self, value: Any, initial_value: Any) -> Any:
        try:
            return self.function(
                *(resolve_if_needed(arg, initial_value) for arg in self.args),
                value,
            )
        except (TypeError, ValueError) as e:
            raise RejectOperations(e) from e


class ImportantFunctionOperation(FunctionOperation):
    important = True
