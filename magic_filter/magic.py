from typing import Any, Callable, Iterable, List, Optional, Pattern, Union

from .attribute import Attribute, resolve_attribute
from .operations import (
    AllFuncOperation,
    AnyFuncOperation,
    AttrOperation,
    ContainsOperation,
    EqualsOperation,
    FuncOperation,
    InOperation,
    NotEqualsOperation,
    RegexpOperation,
)


class MagicFilter:
    def __init__(self, chain: Optional[List[Attribute]] = None) -> None:
        if chain is None:
            chain = []
        self._chain = chain

    def __call__(self, obj: Any) -> bool:
        value = resolve_attribute(self, obj)
        return value is not None

    def __getitem__(self, item: str) -> "MagicFilter":
        attr = Attribute.parse(item)
        return MagicFilter(chain=self._chain + [attr])

    def __getattr__(self, item: str) -> "MagicFilter":
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

    def __matmul__(self, values: Iterable[Any]) -> InOperation:
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

    def func(self, value: Callable[..., Any]) -> FuncOperation:
        """
        Execute any callable on value
        """
        return FuncOperation(value=value, magic=self)

    def all(self, *call: Callable[[Any, Any], bool]) -> AllFuncOperation:
        """
        Analog of builtin all(Iterable[Any])
        """
        return AllFuncOperation(value=call, magic=self)

    def any(self, *call: Callable[[Any, Any], bool]) -> AnyFuncOperation:
        """
        Analog of builtin any(Iterable[Any])
        """
        return AnyFuncOperation(value=call, magic=self)

    # PRIVATE API
    def get_chain(self) -> List[Attribute]:
        return self._chain

    __slots__ = ("_chain",)


F = MagicFilter()
