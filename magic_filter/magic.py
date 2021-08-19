import operator
import re
from functools import wraps
from typing import Any, Callable, Optional, Pattern, Sequence, Tuple, Union

from magic_filter.exceptions import RejectOperations, SwitchModeToAll, SwitchModeToAny
from magic_filter.operations import (
    BaseOperation,
    CallOperation,
    CombinationOperation,
    ComparatorOperation,
    FunctionOperation,
    GetAttributeOperation,
    GetItemOperation,
    RCombinationOperation,
)
from magic_filter.operations.function import ImportantFunctionOperation


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

    def _replace_last(self, operation: BaseOperation) -> "MagicFilter":
        return self._new(self._operations[:-1] + (operation,))

    def _exclude_last(self) -> "MagicFilter":
        return self._new(self._operations[:-1])

    def _resolve(self, value: Any, operations: Optional[Tuple[BaseOperation, ...]] = None) -> Any:
        initial_value = value
        if operations is None:
            operations = self._operations
        rejected = False
        for index, operation in enumerate(operations):
            if rejected and not operation.important:
                continue
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
            except RejectOperations:
                rejected = True
                value = None
                continue
            rejected = False
        return value

    def resolve(self, value: Any) -> Any:
        return self._resolve(value=value)

    def __getattr__(self, item: Any) -> "MagicFilter":
        return self._extend(GetAttributeOperation(name=item))

    attr_ = __getattr__

    def __getitem__(self, item: Any) -> "MagicFilter":
        return self._extend(GetItemOperation(key=item))

    def __eq__(self, other: Any) -> "MagicFilter":  # type: ignore
        return self._extend(ComparatorOperation(right=other, comparator=operator.eq))

    def __ne__(self, other: Any) -> "MagicFilter":  # type: ignore
        return self._extend(ComparatorOperation(right=other, comparator=operator.ne))

    def __lt__(self, other: Any) -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.lt))

    def __gt__(self, other: Any) -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.gt))

    def __le__(self, other: Any) -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.le))

    def __ge__(self, other: Any) -> "MagicFilter":
        return self._extend(ComparatorOperation(right=other, comparator=operator.ge))

    def __invert__(self) -> "MagicFilter":
        if (
            self._operations
            and isinstance(self._operations[-1], ImportantFunctionOperation)
            and self._operations[-1].function == operator.not_
        ):
            return self._exclude_last()
        return self._extend(ImportantFunctionOperation(function=operator.not_))

    def __call__(self, *args: Any, **kwargs: Any) -> "MagicFilter":
        return self._extend(CallOperation(args=args, kwargs=kwargs))

    def __and__(self, other: Any) -> "MagicFilter":
        if isinstance(other, MagicFilter):
            return self._extend(CombinationOperation.and_op(right=other))
        return self._extend(CombinationOperation(right=other, combinator=operator.and_))

    def __rand__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.and_))

    def __or__(self, other: Any) -> "MagicFilter":
        if isinstance(other, MagicFilter):
            return self._extend(CombinationOperation.or_op(right=other))
        return self._extend(CombinationOperation(right=other, combinator=operator.or_))

    def __ror__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.or_))

    def __xor__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.xor))

    def __rxor__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.xor))

    def __rshift__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.rshift))

    def __rrshift__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.rshift))

    def __lshift__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.lshift))

    def __rlshift__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.lshift))

    def __add__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.add))

    def __radd__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.add))

    def __sub__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.sub))

    def __rsub__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.sub))

    def __mul__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.mul))

    def __rmul__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.mul))

    def __truediv__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.truediv))

    def __rtruediv__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.truediv))

    def __floordiv__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.floordiv))

    def __rfloordiv__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.floordiv))

    def __mod__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.mod))

    def __rmod__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.mod))

    def __matmul__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.matmul))

    def __rmatmul__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.matmul))

    def __pow__(self, other: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=other, combinator=operator.pow))

    def __rpow__(self, other: Any) -> "MagicFilter":
        return self._extend(RCombinationOperation(left=other, combinator=operator.pow))

    def __pos__(self) -> "MagicFilter":
        return self._extend(FunctionOperation(function=operator.pos))

    def __neg__(self) -> "MagicFilter":
        return self._extend(FunctionOperation(function=operator.neg))

    def is_(self, value: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=value, combinator=operator.is_))

    def is_not(self, value: Any) -> "MagicFilter":
        return self._extend(CombinationOperation(right=value, combinator=operator.is_not))

    def in_(self, iterable: Sequence[Any]) -> "MagicFilter":
        return self._extend(FunctionOperation.in_op(iterable))

    def contains(self, value: Any) -> "MagicFilter":
        return self._extend(FunctionOperation.contains_op(value))

    def len(self) -> "MagicFilter":
        return self._extend(FunctionOperation(len))

    def regexp(self, pattern: Union[str, Pattern[str]]) -> "MagicFilter":
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        return self._extend(FunctionOperation(pattern.match))

    def func(self, func: Callable[[Any], Any]) -> "MagicFilter":
        return self._extend(FunctionOperation(func))
