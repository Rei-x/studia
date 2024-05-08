"""Testing script for the task."""

import numpy as np
import pytest

from optimization_nelder_mead import (
    rosenbrock_function,
    shrink,
    contract,
    expand,
    reflect,
    run_nelder_mead,
    Simplex2D,
)


def sphere_function(x: np.ndarray) -> float:
    return np.sum(np.square(x))


@pytest.mark.parametrize(
    "point, centroid, alpha",
    [
        (np.array([1]), np.array([0]), 0.0),
        (np.array([1, 1]), np.array([0, 0]), -5.0),
    ],
)
def test_reflect_incorrect_alpha_value(point, centroid, alpha):
    with pytest.raises(ValueError) as excinfo:
        reflect(point, centroid, alpha)
    assert "Invalid value of alpha parameter. Alpha must be greater than 0!" in str(
        excinfo.value
    )


@pytest.mark.parametrize(
    "point, centroid, alpha, exp_val",
    [
        (np.array([1]), np.array([0]), 1.0, np.array([-1])),
        (np.array([1, 1]), np.array([0, 0]), 1.0, np.array([-1, -1])),
        (
            np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            1.0,
            np.array([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]),
        ),
        (np.array([1, 1]), np.array([0, 0]), 3.0, np.array([-3, -3])),
        (np.array([1, 1]), np.array([1, 1]), 1.0, np.array([1, 1])),
        (np.array([1, 1]), np.array([2, 2]), 1.0, np.array([3, 3])),
    ],
)
def test_reflect(point, centroid, alpha, exp_val):
    np.testing.assert_array_equal(exp_val, reflect(point, centroid, alpha))


@pytest.mark.parametrize(
    "point, centroid, gamma",
    [
        (np.array([1]), np.array([0]), 0.0),
        (np.array([1, 1]), np.array([0, 0]), -5.0),
        (np.array([1, 1]), np.array([0, 0]), 1.0),
    ],
)
def test_expand_incorrect_gamma_value(point, centroid, gamma):
    with pytest.raises(ValueError) as excinfo:
        expand(point, centroid, gamma)
    assert "Invalid value of gamma parameter. Gamma must be greater than 1!" in str(
        excinfo.value
    )


@pytest.mark.parametrize(
    "point, centroid, gamma, exp_val",
    [
        (np.array([1]), np.array([0]), 2.0, np.array([2])),
        (np.array([1, 1]), np.array([0, 0]), 2.0, np.array([2, 2])),
        (
            np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            2.0,
            np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
        ),
        (np.array([1, 1]), np.array([0, 0]), 3.0, np.array([3, 3])),
    ],
)
def test_expand(point, centroid, gamma, exp_val):
    np.testing.assert_array_equal(exp_val, expand(point, centroid, gamma))


@pytest.mark.parametrize(
    "point, centroid, beta",
    [
        (np.array([1]), np.array([0]), 0.0),
        (np.array([1, 1]), np.array([0, 0]), 1.0),
        (np.array([1]), np.array([0]), 2.0),
        (np.array([1, 1]), np.array([0, 0]), -3.0),
    ],
)
def test_contract_incorrect_beta_value(point, centroid, beta):
    with pytest.raises(ValueError) as excinfo:
        contract(point, centroid, beta)
    assert "Invalid value of beta parameter. Beta must be in range (0,1)!" in str(
        excinfo.value
    )


@pytest.mark.parametrize(
    "point, centroid, beta, exp_val",
    [
        (np.array([1]), np.array([0]), 0.5, np.array([0.5])),
        (np.array([1, 1]), np.array([0, 0]), 0.5, np.array([0.5, 0.5])),
        (
            np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            0.5,
            np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
        ),
        (np.array([1, 1]), np.array([0, 0]), 0.75, np.array([0.75, 0.75])),
    ],
)
def test_contract(point, centroid, beta, exp_val):
    np.testing.assert_array_equal(exp_val, contract(point, centroid, beta))


@pytest.mark.parametrize(
    "simplex, sigma",
    [
        (np.array([[1], [2], [3]]), 0.0),
        (np.array([[1], [2], [3]]), 1.0),
        (np.array([[1], [2], [3]]), 2.0),
        (np.array([[1], [2], [3]]), -3.0),
    ],
)
def test_shrink_incorrect_sigma_value(simplex, sigma):
    with pytest.raises(ValueError) as excinfo:
        shrink(simplex, sigma)
    assert "Invalid value of sigma parameter. Sigma must be in range (0,1)!" in str(
        excinfo.value
    )


@pytest.mark.parametrize(
    "simplex, sigma, exp_val",
    [
        (np.array([[1], [2], [3]]), 0.5, np.array([[1], [1.5], [2]])),
        (
            np.array([[1, 1], [2, 2], [3, 3]]),
            0.5,
            np.array([[1, 1], [1.5, 1.5], [2, 2]]),
        ),
    ],
)
def test_shrink(simplex, sigma, exp_val):
    np.testing.assert_array_equal(exp_val, shrink(simplex, sigma))


@pytest.mark.parametrize(
    "initial_simplex, expected_optimum",
    [
        (
            Simplex2D([-1.5, -1.5], [-1.0, -1.5], [-1.5, 0.0], rosenbrock_function),
            np.array([1.0, 1.0]),
        ),
        (
            Simplex2D([-1.0, -1.0], [0.0, 3.5], [1.5, 0.0], rosenbrock_function),
            np.array([1.0, 1.0]),
        ),
        (
            Simplex2D([-1.0, -1.0], [0.0, 3.5], [1.5, 0.0], sphere_function),
            np.array([0.0, 0.0]),
        ),
        (
            Simplex2D([10.0, 100.0], [-30.0, 70.0], [100.0, -50.0], sphere_function),
            np.array([0.0, 0.0]),
        ),
    ],
)
def test_run_nelder_mead_rosenbrock(initial_simplex, expected_optimum):
    optimum_point, _ = run_nelder_mead(initial_simplex)
    np.testing.assert_array_almost_equal(optimum_point, expected_optimum, decimal=5)
