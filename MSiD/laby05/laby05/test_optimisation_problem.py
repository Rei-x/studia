"""Testing script for the task."""

from typing import Tuple

import numpy as np
import pytest

from optimisation_problem import (
    constr_filler,
    constr_flesh,
    constr_salt,
    constr_x_2,
    income,
    optimise,
)

x_1_test = [33, -10, 96, 22, 96]
x_2_test = [56, 60, -34, -51, -21]


def get_test_val(idx: int) -> Tuple[int, int]:
    """Aux function to return tested decision values."""
    test_solutions = np.array([x_1_test, x_2_test])
    return tuple(test_solutions.T[idx])


@pytest.mark.parametrize(
    "x_1, x_2, exp_val",
    [
        (*get_test_val(0), 1829),
        (*get_test_val(1), 1370),
        (*get_test_val(2), 398),
        (*get_test_val(3), -989),
        (*get_test_val(4), 723),
    ],
)
def test_income(x_1, x_2, exp_val):
    np.testing.assert_almost_equal(income(x_1=x_1, x_2=x_2), exp_val, 2)


@pytest.mark.parametrize(
    "x_1, x_2, exp_val",
    [
        (*get_test_val(0), 489.0),
        (*get_test_val(1), 503.33),
        (*get_test_val(2), 468.0),
        (*get_test_val(3), 492.66),
        (*get_test_val(4), 468.0),
    ],
)
def test_constr_filler(x_1, x_2, exp_val):
    np.testing.assert_almost_equal(constr_filler([x_1, x_2]), exp_val, 2)


@pytest.mark.parametrize(
    "x_1, x_2, exp_val",
    [
        (*get_test_val(0), 933.1),
        (*get_test_val(1), 951.0),
        (*get_test_val(2), 982.6),
        (*get_test_val(3), 1034.9),
        (*get_test_val(4), 970.9),
    ],
)
def test_constr_flesh(x_1, x_2, exp_val):
    np.testing.assert_almost_equal(constr_flesh([x_1, x_2]), exp_val, 2)


@pytest.mark.parametrize(
    "x_1, x_2, exp_val",
    [
        (*get_test_val(0), 238.9),
        (*get_test_val(1), 245.67),
        (*get_test_val(2), 237.4),
        (*get_test_val(3), 251.43),
        (*get_test_val(4), 236.1),
    ],
)
def test_constr_salt(x_1, x_2, exp_val):
    np.testing.assert_almost_equal(constr_salt([x_1, x_2]), exp_val, 2)


@pytest.mark.parametrize(
    "x_1, x_2",
    [
        get_test_val(0),
        get_test_val(1),
        get_test_val(2),
        get_test_val(3),
        get_test_val(4),
    ],
)
def test_constr_x_2(x_1, x_2):
    np.testing.assert_almost_equal(constr_x_2([x_1, x_2]), x_2, 2)


def test_optimise():
    np.testing.assert_almost_equal(
        optimise(), np.array([425.09202593, 874.94887448]), decimal=2
    )
