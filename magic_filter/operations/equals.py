from typing import Any

from .simple import SimpleOperation


class EqualsOperation(SimpleOperation):
    def resolve(self, value: Any) -> bool:
        return value == self.value  # type: ignore


class NotEqualsOperation(EqualsOperation):
    def resolve(self, value: Any) -> bool:
        return not super().resolve(value=value)
