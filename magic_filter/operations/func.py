from typing import Any, cast

from .simple import SimpleOperation


class FuncOperation(SimpleOperation):
    def resolve(self, value: Any) -> bool:
        return cast(bool, self.value(value))
