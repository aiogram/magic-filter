from typing import Any

from .func import FuncOperation


class ContainsOperation(FuncOperation):
    op = "contains"

    def resolve(self, value: Any) -> bool:
        return self.value in value
