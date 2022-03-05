from typing import Any


def in_op(a: Any, b: Any) -> bool:
    try:
        return b in a
    except TypeError:
        return False


def contains_op(a: Any, b: Any) -> bool:
    try:
        return a in b
    except TypeError:
        return False


def and_op(a: Any, b: Any) -> Any:
    return a and b


def or_op(a: Any, b: Any) -> Any:
    return a or b
