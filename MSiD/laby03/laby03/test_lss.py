import lss
import numpy as np
import pytest


X, Y = lss.read_data_vectors()


@pytest.mark.parametrize(
    "polynomial_degree, exp_result",
    [
        (0, np.array([[0]])),
        (1, np.array([[0], [1]])),
        (2, np.array([[0], [1], [2]])),
        (3, np.array([[0], [1], [2], [3]])),
    ],
)
def test_polynomial_form(polynomial_degree, exp_result):
    np.testing.assert_array_equal(
        lss.get_polynomial_form(polynomial_degree), exp_result
    )


@pytest.mark.parametrize(
    "theta, precission, exp_result",
    [
        (
            np.array([[1.86548519e00], [0.33807518e-02], [-1.04156655e-05]]),
            3,
            "1.865*x^0 + 0.003*x^1 + -0.0*x^2",
        ),
        (
            np.array(
                [
                    [4.35169575e01],
                    [1.30404047e-03],
                    [-3.50173017e-08],
                    [3.55083643e-13],
                    [-7.97290264e-19],
                    [-3.88362946e-24],
                ]
            ),
            5,
            "43.51696*x^0 + 0.0013*x^1 + -0.0*x^2 + 0.0*x^3 + -0.0*x^4 + -0.0*x^5",
        ),
        (
            np.array([[19.5666359], [0.20026391]]),
            1,
            "19.6*x^0 + 0.2*x^1",
        ),
    ],
)
def test_print_polynomial(theta, precission, exp_result):
    assert lss.print_polynomial(theta, precission) == exp_result


@pytest.mark.parametrize(
    "polynomial_degree, exp_result",
    [
        (0, np.array([[6.49565714]])),
        (1, np.array([[5.57619059], [0.0088007]])),
        (2, np.array([[4.86548519e00], [2.33807518e-02], [-5.04156655e-05]])),
        (
            3,
            np.array(
                [[4.79214481e00], [2.58358036e-02], [-6.95863178e-05], [3.94648205e-08]]
            ),
        ),
        (
            4,
            np.array(
                [
                    [4.99949649e00],
                    [1.57674472e-02],
                    [6.45111445e-05],
                    [-5.99332140e-07],
                    [9.72509213e-10],
                ]
            ),
        ),
        (
            5,
            np.array(
                [
                    [4.22887997e00],
                    [6.80849677e-02],
                    [-1.01662102e-03],
                    [8.48670958e-06],
                    [-3.16066573e-08],
                    [4.12017807e-11],
                ]
            ),
        ),
    ],
)
def test_least_squares_solution(polynomial_degree, exp_result):
    np.testing.assert_almost_equal(
        lss.least_squares_solution(X, Y, polynomial_degree), exp_result, decimal=4
    )
