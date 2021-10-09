from magic_filter import AttrDict


class TestAttrDict:
    def test_attrdict(self):
        attr = AttrDict({"a": 1, "b": 2, "c": "d"})

        assert attr["a"] == 1
        assert attr.a == 1

        assert attr["b"] == 2
        assert attr.b == 2

        assert attr["c"] == "d"
        assert attr.c == "d"
