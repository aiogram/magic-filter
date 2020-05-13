from typing import TYPE_CHECKING, Any, Callable

from .simple import SimpleOperation

if TYPE_CHECKING:
    from ..magic import MagicFilter


class AttrOperation(SimpleOperation):
    def __init__(self, operation: Callable[..., bool], value: Any, magic: MagicFilter) -> None:
        super().__init__(value=value, magic=magic)
        self.operation = operation

    def resolve(self, value: Any) -> bool:
        return self.operation(value, self.value)
