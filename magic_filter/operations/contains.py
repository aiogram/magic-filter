from typing import Any

from .func import FuncOperation


class ContainsOperation(FuncOperation):
    def resolve(self, value: Any) -> bool:
        return self.value in value
