from collections import namedtuple

import pytest

from magic_filter import F

User = namedtuple("User", ["age", "about", "job"])
Job = namedtuple("Job", ["place", "salary", "position"])


@pytest.fixture(name="user")
def user():
    yield User(
        age=19,
        about="Gonna fly to the 'Factory'",
        job=Job(place="New York", salary=200_000, position="lead architect"),
    )


class TestMagicFilter:
    @pytest.mark.parametrize(
        "case",
        [
            F.age == 19,
            F.about__lower == "gonna fly to the 'factory'",
            F.job.place == "New York",
            F.job.place__len == 8,
            F.job.salary == 200_000,
        ],
    )
    def test_equals(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize(
        "case", [~(F.age == 42), F.age != 42, F.job.place != "Moscow", F.job.place__len != 5]
    )
    def test_not_equals(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize("case", [F.age, F.job, ~F.test])
    def test_not_none(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize(
        "case",
        [
            F.job.position__lower @ ("lead architect",),
            F.age @ range(15, 40),
            F.job.place.in_("New York", "WDC"),
            F.age @ iter(range(30)),
        ],
    )
    def test_operation_in_(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize(
        "case", [F.about.regexp(r"Gonna .+"), F.about.regexp(r".+")],
    )
    def test_regexp(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize(
        "case", [F.about.contains("Factory"), F.job.place__lower.contains("n")]
    )
    def test_contains(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize("case", [F.job.place.startswith("New")])
    def test_startswith(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize("case", [F.job.position.endswith("architect")])
    def test_endswith(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize("case", [F.age.func(lambda v: v in range(142))])
    def test_func(self, case, user: User):
        assert case(user)

    @pytest.mark.parametrize("case", [F.job.place__test == "NEW YORK"])
    def test_unknown_modifiers(self, case, user: User):
        assert not case(user)

    @pytest.mark.parametrize("case", [F.age__lower == "19", F.age__len == 2])
    def test_modifier_error(self, case, user: User):
        with pytest.raises(ValueError):
            assert case(user)

    @pytest.mark.parametrize(
        "case",
        [
            (F.age == 19) & (F.about.contains("Factory")),
            (F.age == 42) | (F.about.contains("Factory")),
            F.age & F.job & F.job.place,
        ],
    )
    def test_combined(self, case, user: User):
        assert case(user)
