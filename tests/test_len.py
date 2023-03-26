import pytest

from magic_filter import F


class TestLen:
    def test_has_no_len(self):
        # F object doesn't have len(). But F.len() can be used,
        # so it will raise error with suggestion to use F.len()
        with pytest.raises(TypeError):
            len(F)
