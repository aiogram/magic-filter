from typing import Any

from .func import FuncOperation


class InOperation(FuncOperation):
    op = "in_"

    def resolve(self, value: Any) -> bool:
        return value in self.value

    def __str__(self) -> str:
        values = ", ".join(map(repr, self.value))
        return f"{self.magic}.{self.op}({values})"
