from typing import Any, cast

from .simple import SimpleOperation


class FuncOperation(SimpleOperation):
    op = "func"

    def resolve(self, value: Any) -> bool:
        return cast(bool, self.value(value))

    def __str__(self) -> str:
        return f"{self.magic}.{self.op}({self.value!r})"
