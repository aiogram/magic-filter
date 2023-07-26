from collections import namedtuple
from typing import Any, NamedTuple, Optional

import pytest

from magic_filter import F, MagicFilter

Job = namedtuple("Job", ["place", "salary", "position"])


class User(NamedTuple):
    age: int
    about: str
    job: Job
    favorite_digits: Optional[str]

    def __matmul__(self, other: Any) -> int:  # for testing
        if isinstance(other, Job):
            return self.job.place == other.place  # User (at) Job
        return NotImplemented

    def resolve(self) -> int:
        return str(self)


another_user = User(
    age=18,
    about="18 y.o. junior dev from NY",
    job=Job(place="New York", salary=200_000, position="junior developer"),
    favorite_digits="test",
)


@pytest.fixture(name="user")
def user():
    yield User(
        age=19,
        about="Gonna fly to the 'Factory'",
        job=Job(place="New York", salary=200_000, position="lead architect"),
        favorite_digits="",
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
            ~(~(F.age != 42)),
            F.age != 42,
            F.job.place != "Hogwarts",
            F.job.place.len() != 5,
            F.job.salary > 100_000,
            F.job.salary < 1_000_000,
            F.job.salary >= 200_000,
            F.job.salary <= 200_000,
            F.age,
            F.job,
            F.age == F.age,
            F.age + 1 == 20,
            5 + F.age - 1 == 42 - F.age,
            19 // F.age == F.age // 19,
            F.job.salary / F.job.salary == 1 * F.age * (1 / F.age),
            F.job.salary % 100 == 0,
            23 % F.age != 0,
            -F.job.salary == -(+F.job.salary),
            1**F.age == F.age * (F.age**-1),
            F.age >> 2 == 1 << (F.job.salary // 100_000),
            (F.age << 2) // 38 == 1_048_576 >> F.age,
            F.age & 16 == 16 & F.age,
            F.age | 4 == 4 | F.age,
            11 ^ F.age == F.age ^ 11,
            F @ F.job,
            another_user @ F.job,
            F.job.is_not(None),
            F.is_(F),
            F.attr_("resolve")().contains("User"),
            F.job.position.lower().in_(("lead architect",)),
            F.age.in_(range(15, 40)),
            F.job.place.in_({"New York", "WDC"}),
            F.age.not_in(range(40, 100)),
            F.about.regexp(r"Gonna .+"),
            F.about.regexp(r".+"),
            F.about.contains("Factory"),
            F.job.place.lower().contains("n"),
            F.job.place.upper().contains("N"),
            F.job.place.upper().not_contains("A"),
            F.job.place.startswith("New"),
            F.job.position.endswith("architect"),
            F.age.func(lambda v: v in range(142)),
            F.job.place.func(str.split, maxsplit=1)[0] == "New",
            (F.age == 19) & (F.about.contains("Factory")),
            (F.age == 42) | (F.about.contains("Factory")),
            F.age & F.job & F.job.place,
            F.about.len() == 26,
            F.about[0] == "G",
            F.about[0].lower() == "g",
            F.about[:5] == "Gonna",
            F.about[:5].lower() == "gonna",
            F.about[:5:2].lower() == "gna",
            F.about[6:9] == "fly",
            ~~F.about[6:9] == "fly",
            F.about[...].islower(),
            ~F.about[:].isdigit(),
            ~F.job.contains("test"),
            F.job[F.salary > 100_000].place == "New York",
            F.job[F.salary > 100_000][F.place == "New York"],
            ~F.job[F.salary < 100_000],
            (F.age.cast(str) + " years" == "19 years"),
        ],
    )
    def test_operations(self, case: MagicFilter, user: User):
        assert case.resolve(user)
        assert F.ilter(case)(user)

    @pytest.mark.parametrize("case", [F.about["test"], F.about[100]])
    def test_invalid_get_item(self, case: MagicFilter, user: User):
        assert not case.resolve(user)
        assert not F.ilter(case)(user)

    @pytest.mark.parametrize(
        "value,a,b",
        [[None, None, True], ["spam", False, True], ["321", True, False], [42, None, True]],
    )
    def test_reject_has_no_attribute(self, value: Any, a: bool, b: bool):
        user = User(
            age=42,
            about="Developer",
            job=Job(position="senior-tomato", place="Italy", salary=300_000),
            favorite_digits=value,
        )
        regular = F.favorite_digits.isdigit()
        inverted = ~regular

        assert regular.resolve(user) is a
        assert inverted.resolve(user) is b

    def test_exclude_mutually_exclusive_inversions(self, user: User):
        case = F.job
        assert len(case._operations) == 1
        case = ~case
        assert len(case._operations) == 2
        case = ~case
        assert len(case._operations) == 1
        case = ~case
        assert len(case._operations) == 2

    def test_extract_operation(self):
        case = F.extract(F > 2)
        assert case.resolve(range(5)) == [3, 4]

        assert not case.resolve(42)

    def test_bool(self):
        case = F.foo.bar.baz
        assert bool(case) is True
