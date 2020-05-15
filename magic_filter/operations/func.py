from typing import Any, cast

from .simple import SimpleOperation


class FuncOperation(SimpleOperation):
    def _resolve(self, value: Any) -> bool:
        return cast(bool, self._value(value))
