from typing import Any

from .all import AllFuncOperation


class AnyFuncOperation(AllFuncOperation):
    op = "any"

    def resolve(self, value: Any) -> bool:
        for item in self.value:
            if item(value):
                return True
        return False
