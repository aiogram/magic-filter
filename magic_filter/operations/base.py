from abc import ABC, abstractmethod
from typing import Any


class BaseOperation(ABC):
    @abstractmethod
    def resolve(self, value: Any, initial_value: Any) -> Any:  # pragma: no cover
        pass
