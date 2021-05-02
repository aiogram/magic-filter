from typing import Any, Dict, Tuple

from .base import BaseOperation


class CallOperation(BaseOperation):
    __slots__ = ("args", "kwargs")

    def __init__(self, args: Tuple[Any, ...], kwargs: Dict[str, Any]):
        self.args = args
        self.kwargs = kwargs

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return value(*self.args, **self.kwargs)
