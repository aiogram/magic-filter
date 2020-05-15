from typing import Any

from .simple import SimpleOperation


class EqualsOperation(SimpleOperation):
    def _resolve(self, value: Any) -> bool:
        return value == self._value  # type: ignore


class NotEqualsOperation(EqualsOperation):
    def _resolve(self, value: Any) -> bool:
        return not super()._resolve(value=value)
