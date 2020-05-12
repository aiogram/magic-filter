import re
from typing import Any

from .func import FuncOperation


class RegexpOperation(FuncOperation):
    op = "regexp"

    def resolve(self, value: Any) -> bool:
        result = re.match(self.value, value)
        return bool(result)
