from typing import Any

from .func import FuncOperation


class ContainsOperation(FuncOperation):
    def _resolve(self, value: Any) -> bool:
        return self._value in value
