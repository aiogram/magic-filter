from collections import namedtuple
from typing import Any

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
            F.about.lower() == "gonna fly to the 'factory'",
            F.job.place == "New York",
            F.job.place.len() == 8,
            F.job.salary == 200_000,
            ~(F.age == 42),
            F.age != 42,
            F.job.place != "Hogwarts",
            F.job.place.len() != 5,
            F.job.salary > 100_000,
            F.job.salary < 1_000_000,
            F.job.salary >= 200_000,
            F.job.salary <= 200_000,
            F.age,
            F.job,
            ~F.test,
            F.job.position.lower().in_(("lead architect",)),
            F.age.in_(range(15, 40)),
            F.job.place.in_({"New York", "WDC"}),
            F.about.regexp(r"Gonna .+"),
            F.about.regexp(r".+"),
            F.about.contains("Factory"),
            F.job.place.lower().contains("n"),
            F.job.place.upper().contains("N"),
            F.job.place.startswith("New"),
            F.job.position.endswith("architect"),
            F.age.func(lambda v: v in range(142)),
            (F.age == 19) & (F.about.contains("Factory")),
            (F.age == 42) | (F.about.contains("Factory")),
            F.age & F.job & F.job.place,
            F.about.len() == 26,
            F.about[0] == "G",
            F.about[0].lower() == "g",
            F.about[:5] == "Gonna",
            F.about[:5].lower() == "gonna",
            F.about[...].islower(),
            ~F.about[:].isdigit(),
        ],
    )
    def test_operations(self, case, user: User):
        assert case.resolve(user)
        assert F.ilter(case)(user)

    @pytest.mark.parametrize("case", [F.about["test"], F.about[100]])
    def test_invalid_get_item(self, case, user: User):
        assert not case.resolve(user)
        assert not F.ilter(case)(user)
