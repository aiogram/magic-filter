from typing import Any, Iterable

from magic_filter.exceptions import SwitchModeToAll, SwitchModeToAny

from .base import BaseOperation


class GetItemOperation(BaseOperation):
    __slots__ = ("key",)

    def __init__(self, key: Any) -> None:
        self.key = key

    def resolve(self, value: Any, initial_value: Any) -> Any:
        if isinstance(value, Iterable):
            if self.key is Any:
                raise SwitchModeToAny()
            if self.key is ...:
                raise SwitchModeToAll()
        try:
            return value[self.key]
        except (KeyError, IndexError, TypeError):
            return None
