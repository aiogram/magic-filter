from typing import Any

from .simple import SimpleOperation


class EqualsOperation(SimpleOperation):
    op = "=="

    def resolve(self, value: Any) -> bool:
        return value == self.value  # type: ignore

    def __str__(self) -> str:
        return f"{self.magic} {self.op} {self.value!r}"


class NotEqualsOperation(EqualsOperation):
    op = "!="

    def resolve(self, value: Any) -> bool:
        return not super().resolve(value=value)
