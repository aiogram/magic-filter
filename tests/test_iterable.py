import pytest

from magic_filter import F


class TestIterable:
    def test_cannot_be_used_as_an_iterable(self):
        # If instance of MagicFilter be an Iterable object it can be used as "zip-bomb"-like object,
        # because `list(F)` can use 100% of the RAM and crash the application.
        with pytest.raises(TypeError):
            list(F)
