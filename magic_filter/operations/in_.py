from typing import Any

from .func import FuncOperation


class InOperation(FuncOperation):
    def resolve(self, value: Any) -> bool:
        return value in self.value
