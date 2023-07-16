import re

import pytest

from magic_filter import F


class TestLen:
    def test_has_no_len(self):
        # F object doesn't have len(). But F.len() can be used,
        # so it will raise error with suggestion to use F.len()
        error_message = "Length can't be taken using len() function. Use MagicFilter.len() instead."
        with pytest.raises(TypeError, match=re.escape(error_message)):
            len(F)
