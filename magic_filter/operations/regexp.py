import re
from typing import Any

from .func import FuncOperation


class RegexpOperation(FuncOperation):
    def _resolve(self, value: Any) -> bool:
        result = re.match(self._value, value)
        return bool(result)
