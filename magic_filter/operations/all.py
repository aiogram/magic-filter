from typing import Any

from .in_ import InOperation


class AllFuncOperation(InOperation):
    op = "all"

    def resolve(self, value: Any) -> bool:
        for item in self.value:
            if item(value):
                return False
        return True

    def __str__(self) -> str:
        values = ", ".join(map(repr, self.value))
        return f"{self.magic}.{self.op}({values})"
