import operator
import re
from functools import wraps
from typing import Any, Callable, Optional, Pattern, Sequence, Tuple, Union

from magic_filter.exceptions import SwitchModeToAll, SwitchModeToAny
from magic_filter.operations import (
    BaseOperation,
    CallOperation,
    CombinationOperation,
    ComparatorOperation,
    FunctionOperation,
    GetAttributeOperation,
    GetItemOperation,
)


class MagicFilter:
    __slots__ = ("_operations",)

    def __init__(self, operations: Tuple[BaseOperation, ...] = ()) -> None:
        self._operations = operations

    @classmethod
    def ilter(cls, magic: "MagicFilter") -> Callable[[Any], Any]:
        @wraps(magic.resolve)
        def wrapper(value: Any) -> Any:
            return magic.resolve(value)

        return wrapper

    @classmethod
    def _new(cls, operations: Tuple[BaseOperation, ...]) -> "MagicFilter":
        return cls(operations=operations)

    def _extend(self, operation: BaseOperation) -> "MagicFilter":
        return self._new(self._operations + (operation,))

    def _resolve(self, value: Any, operations: Optional[Tuple[BaseOperation, ...]] = None) -> Any:
        initial_value = value
        if operations is None:
            operations = self._operations
        for index, operation in enumerate(operations):
            try:
                value = operation.resolve(value=value, initial_value=initial_value)
            except SwitchModeToAll:
                return all(
                    self._resolve(value=item, operations=operations[index + 1 :]) for item in value
                )
            except SwitchModeToAny:
                return any(
                    self._resolve(value=item, operations=operations[index + 1 :]) for item in value
                )
        return value

    def resolve(self, value: Any) -> Any:
        return self._resolve(value=value)

    def __getattr__(self, item: Any) -> "MagicFilter":
        return self._extend(GetAttributeOperation(name=item))

    attr_ = __getattr__

    def __getitem__(self, item: Any) -> "MagicFilter":
        return self._extend(GetItemOperation(key=item))

    def __eq__(self, other: "MagicFilter") -> "MagicFilter":  # type: ignore
        return self._extend(ComparatorOperation(right=other, comparator=operator.eq))

    def __ne__(self, other: "MagicFilter") -> "MagicFilter":  # type: ignore
        return self._extend(ComparatorOperation(right=other, comparator=operator.ne))

    def __lt__(self, other: "MagicFilter") -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.lt))

    def __gt__(self, other: "MagicFilter") -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.gt))

    def __le__(self, other: "MagicFilter") -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.le))

    def __ge__(self, other: "MagicFilter") -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.ge))

    def __invert__(self) -> "MagicFilter":
        return self._extend(FunctionOperation(function=operator.not_))

    def __call__(self, *args: Any, **kwargs: Any) -> "MagicFilter":
        return self._extend(CallOperation(args=args, kwargs=kwargs))

    def __and__(self, other: "MagicFilter") -> "MagicFilter":
        return self._extend(CombinationOperation.and_op(right=other))

    def __or__(self, other: "MagicFilter") -> "MagicFilter":
        return self._extend(CombinationOperation.or_op(right=other))

    def in_(self, iterable: Sequence[Any]) -> "MagicFilter":
        return self._extend(FunctionOperation.in_op(iterable))

    def contains(self, value: Sequence[Any]) -> "MagicFilter":
        return self._extend(FunctionOperation.contains_op(value))

    def len(self) -> "MagicFilter":
        return self._extend(FunctionOperation(len))

    def regexp(self, pattern: Union[str, Pattern[str]]) -> "MagicFilter":
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        return self._extend(FunctionOperation(pattern.match))

    def func(self, func: Callable[[Any], Any]) -> "MagicFilter":
        return self._extend(FunctionOperation(func))
