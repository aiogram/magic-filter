from typing import Any

from .func import FuncOperation


class InOperation(FuncOperation):
    def _resolve(self, value: Any) -> bool:
        return value in self._value
