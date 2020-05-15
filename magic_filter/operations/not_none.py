from typing import Any

from .simple import SimpleOperation


class NotNoneOperation(SimpleOperation):
    def _resolve(self, value: Any) -> bool:
        return value is not None
