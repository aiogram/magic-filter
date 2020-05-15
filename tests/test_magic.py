from collections import namedtuple

from magic_filter import MagicFilter

User = namedtuple("User", ["age", "about", "job"])
Job = namedtuple("User", ["place", "salary", "position"])


class TestMagicFilter:
    def test_equals(self):
        ...

    def test_not_equals(self):
        ...

    def test_operation_in_(self):
        f = MagicFilter()

        user = User(
            age=19,
            about="Gonna fly to the 'Factory'",
            job=Job(place="New York", salary=200_000, position="lead architect"),
        )

        assert not (f.job.position__lower @ ("designer",))(user)
        assert (f.age @ range(15, 40))(user)
        assert f.job.place.in_("New York", "WDC")
        assert f.age @ iter(range(30))

    def test_regexp(self):
        ...

    def test_contains(self):
        ...

    def test_startswith(self):
        ...

    def test_endswith(self):
        ...

    def test_func(self):
        ...

    def test_all(self):
        ...

    def test_any(self):
        ...
