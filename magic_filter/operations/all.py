from typing import Any

from .in_ import InOperation


class AllFuncOperation(InOperation):
    def resolve(self, value: Any) -> bool:
        for item in self.value:
            if item(value):
                return False
        return True
