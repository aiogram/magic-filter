from typing import Any, Sequence, Set, Union


def in_op(a: Union[Sequence[Any], Set[Any]], b: Any) -> bool:
    try:
        return b in a
    except TypeError:
        return False


def contains_op(a: Any, b: Union[Sequence[Any], Set[Any]]) -> bool:
    try:
        return a in b
    except TypeError:
        return False


def and_op(a: Any, b: Any) -> Any:
    return a and b


def or_op(a: Any, b: Any) -> Any:
    return a or b
