from __future__ import annotations

from functools import reduce
from typing import Any, Callable, List, Optional, Pattern, Sequence, Union

from .attribute import Attribute
from .operations import (
    AllFuncOperation,
    AnyFuncOperation,
    AttrOperation,
    ContainsOperation,
    DataType,
    EqualsOperation,
    FuncOperation,
    InOperation,
    NotEqualsOperation,
    RegexpOperation,
)


class MagicFilter:
    def __init__(
        self, chain: Optional[List[Attribute]] = None, name: Optional[str] = None
    ) -> None:
        self._name = name
        if chain is None:
            chain = []
        self.chain = chain

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = self.__class__.__name__
        return self._name

    def run(self, obj: Any) -> bool:
        """
        Main entry point
        """
        value = self.resolve_attribute(obj)
        return value is not None

    def __call__(self, obj: Any) -> bool:
        return self.run(obj=obj)

    def resolve_attribute(self, obj: Any) -> Any:
        return reduce(self._resolver, self.chain, obj)

    def _resolver(self, item: Any, attr: Attribute) -> Any:  # NOQA: Method may be static
        result = getattr(item, attr.name)
        if attr.modifiers:
            for modifier in attr.modifiers:
                try:
                    mod = getattr(attr, f"modifier_{modifier}")
                except AttributeError:
                    raise AttributeError(f"{modifier!r} modifier is not supported")
                result = mod(result)
        return result

    def __str__(self) -> str:
        return ".".join(map(str, [self.name] + self.chain))  # type: ignore

    def __getitem__(self, item: str) -> MagicFilter:
        attr = Attribute.parse(item)
        return MagicFilter(name=self.name, chain=self.chain + [attr])

    def __getattr__(self, item: str) -> MagicFilter:
        return self[item]

    def equals(self, value: Any) -> EqualsOperation:
        return EqualsOperation(value=value, magic=self)

    def __eq__(self, value: Any) -> EqualsOperation:  # type: ignore
        return self.equals(value=value)

    def not_equals(self, value: Any) -> NotEqualsOperation:
        return NotEqualsOperation(value=value, magic=self)

    def __ne__(self, value: Any) -> NotEqualsOperation:  # type: ignore
        return self.not_equals(value)

    def in_(self, *values: Any) -> InOperation:
        return InOperation(value=set(values), magic=self)

    def __matmul__(self, values: Sequence[Any]) -> InOperation:
        return self.in_(*values)

    def regexp(self, value: Union[str, Pattern[str]]) -> RegexpOperation:
        return RegexpOperation(value=value, magic=self)

    def contains(self, value: Any) -> ContainsOperation:
        return ContainsOperation(value=value, magic=self)

    def startswith(self, value: str) -> AttrOperation:
        """
        Check the string starts with value
        """
        return AttrOperation(operation=str.startswith, value=value, magic=self)

    def endswith(self, value: str) -> AttrOperation:
        """
        Check the string ends with value
        """
        return AttrOperation(operation=str.endswith, value=value, magic=self)

    def func(self, func: Callable[..., Any]) -> FuncOperation:
        """
        Execute any callable on value
        """
        return FuncOperation(value=func, magic=self)

    def all(self, *call: Callable[[Any, DataType], bool]) -> AllFuncOperation:
        """
        Analog of builtin all(Iterable[Any])
        """
        return AllFuncOperation(value=call, magic=self)

    def any(self, *call: Callable[[Any, DataType], bool]) -> AnyFuncOperation:
        """
        Analog of builtin any(Iterable[Any])
        """
        return AnyFuncOperation(value=call, magic=self)


F = MagicFilter(name="F")
