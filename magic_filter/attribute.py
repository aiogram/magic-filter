from functools import reduce
from typing import Any, Iterable, List, Optional, Sized, Tuple, Type, TypeVar

T = TypeVar("T", bound="Attribute")


class Attribute:
    name: str
    modifiers: Tuple[str, ...]

    def __init__(self, name: str, modifiers: Optional[Iterable[str]]) -> None:
        self.name = name

        if isinstance(modifiers, Iterable):
            modifiers = tuple(modifiers)

        self.modifiers = modifiers or ()

    @classmethod
    def parse(cls: Type[T], value: str) -> T:
        name, *modifiers = value.split("__")
        return cls(name=name, modifiers=modifiers)

    @classmethod
    def modifier_lower(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"Value for modifier `lower` should be type 'str' not {type(value)}")
        return value.casefold()

    @classmethod
    def modifier_len(cls, value: Sized) -> int:
        if not isinstance(value, Sized):
            raise ValueError("Value for modifier `len` should be sized")
        return len(value)

    __slots__ = ("name", "modifiers")


def _resolver(item: Any, attr: Attribute) -> Any:
    result = getattr(item, attr.name)
    if attr.modifiers:
        for modifier in attr.modifiers:
            try:
                modifier_func = getattr(attr, f"modifier_{modifier}")
            except AttributeError:
                raise AttributeError(f"{modifier!r} modifier is not supported")
            result = modifier_func(result)
    return result


def resolve_attribute(obj: Any, chain: List[Attribute]) -> Any:
    return reduce(_resolver, chain, obj)
