from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

DataType = Dict[str, Any]
T = TypeVar("T")
LeftOperand = TypeVar("LeftOperand", bound="BaseOperation")
RightOperand = TypeVar("RightOperand", bound="BaseOperation")


class BaseOperation(ABC):
    op: str = ""

    def __init__(self, value: Any) -> None:
        self.value = value

    def __invert__(self: LeftOperand) -> NotOperation[LeftOperand]:
        return NotOperation(value=self)

    def __and__(self: LeftOperand, other: RightOperand) -> AndOperation[LeftOperand, RightOperand]:
        return AndOperation(value=self, other_value=other)

    def __or__(self: LeftOperand, other: RightOperand) -> OrOperation[LeftOperand, RightOperand]:
        return OrOperation(value=self, other_value=other)

    @abstractmethod
    def run(self, obj: Any) -> bool:
        pass

    def __call__(self, obj: Any) -> bool:
        return self.run(obj=obj)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(value={self.value!r})>"


class AndOperation(BaseOperation, Generic[LeftOperand, RightOperand]):
    op = "&"

    def __init__(self, value: LeftOperand, other_value: RightOperand) -> None:
        super().__init__(value=value)
        self.other_value = other_value

    def run(self, obj: Any) -> bool:
        return self.value.run(obj=obj) and self.other_value.run(obj=obj)

    def __str__(self) -> str:
        return f"({self.value}) {self.op} ({self.other_value})"


class OrOperation(AndOperation[LeftOperand, RightOperand]):
    op = "|"

    def run(self, obj: Any) -> bool:
        return self.value.run(obj) or self.other_value.run(obj)


class NotOperation(BaseOperation, Generic[LeftOperand]):
    value: LeftOperand
    op = "~"

    def run(self, obj: Any) -> bool:
        return not self.value.run(obj)

    def __str__(self) -> str:
        return f"{self.op}({self.value})"
