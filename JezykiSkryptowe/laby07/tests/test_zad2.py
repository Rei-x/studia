import pytest

from laby07.zad2 import atleast, atmost, exists, forall


@pytest.mark.parametrize(
    "pred, iterable, expected",
    [
        (lambda x: x > 0, [1, 2, 3, 4, 5], True),
        (lambda x: x > 0, [1, 2, -3, 4, 5], False),
        (lambda x: x % 2 == 0, [], True),
    ],
)
def test_forall(pred, iterable, expected):
    assert forall(pred, iterable) == expected


@pytest.mark.parametrize(
    "pred, iterable, expected",
    [
        (lambda x: x > 0, [1, 2, 3, 4, 5], True),
        (lambda x: x > 0, [-1, -2, -3, -4, -5], False),
        (lambda x: x % 2 == 0, [1, 3, 5], False),
        (lambda x: x % 2 == 0, [], False),
    ],
)
def test_exists(pred, iterable, expected):
    assert exists(pred, iterable) == expected


@pytest.mark.parametrize(
    "n, pred, iterable, expected",
    [
        (3, lambda x: x > 0, [1, 2, 3, 4, 5], True),
        (2, lambda x: x > 0, [-1, 2, -3, 4, 5], True),
        (2, lambda x: x % 2 == 0, [1, 3, 5], False),
        (0, lambda x: x % 2 == 0, [], True),
    ],
)
def test_atleast(n, pred, iterable, expected):
    assert atleast(n, pred, iterable) == expected


@pytest.mark.parametrize(
    "n, pred, iterable, expected",
    [
        (3, lambda x: x > 0, [1, 2, 3, 4, 5], False),
        (2, lambda x: x > 0, [-1, 2, -3, 4, 5], False),
        (2, lambda x: x % 2 == 0, [1, 3, 5], True),
        (0, lambda x: x % 2 == 0, [1, 3, 5], True),
    ],
)
def test_atmost(n, pred, iterable, expected):
    assert atmost(n, pred, iterable) == expected
