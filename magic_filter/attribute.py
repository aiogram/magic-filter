from dataclasses import dataclass
from typing import List, Optional, Sized, Type, TypeVar

T = TypeVar("T", bound="Attribute")


@dataclass
class Attribute:
    name: str
    modifiers: Optional[List[str]] = None

    def __str__(self) -> str:
        parts = [self.name]
        if self.modifiers:
            parts.extend(self.modifiers)
        return "__".join(parts)

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
