"""Main script for the task."""

from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from scipy import optimize


# ########## Definition of the optimisation problem ##########
# Implement functions below so that tests are able to pass.
# ############################################################


def income(x_1: float, x_2: float) -> float:
    """Income from production of flesh."""
    return x_1 * 13 + x_2 * 25


def objective(decision_vars: Tuple[float, float]) -> float:
    """Objective function (i.e. adapted income to optimisation jargon)."""
    x_1, x_2 = decision_vars
    return -income(x_1, x_2)


def constr_flesh(decision_vars: Tuple[float, float]) -> float:
    """Constraint according to substrate: flesh."""
    return 1000 - decision_vars[0] * 1 / 2 - decision_vars[1] * 9 / 10


def constr_filler(decision_vars: Tuple[float, float]) -> float:
    """Constraint according to substrate: filler."""
    return 500 - decision_vars[0] * 1 / 3


def constr_salt(decision_vars: Tuple[float, float]) -> float:
    """Constraint according to substrate: salt."""
    return 250 - decision_vars[0] * 1 / 6 - decision_vars[1] * 1 / 10


def constr_x_1(decision_vars: Tuple[float, float]) -> float:
    """Constraint according to x_1 decision variable."""
    x_1, _ = decision_vars
    return x_1


def constr_x_2(decision_vars: Tuple[float, float]) -> float:
    """Constraint according to x_1 decision variable."""
    _, x_2 = decision_vars
    return x_2


def optimise() -> Tuple[float, float]:
    """Main optimisation method."""
    x_1, x_2 = 0, 0
    x_opt = optimize.fmin_cobyla(
        func=objective,
        x0=(x_1, x_2),
        cons=[constr_filler, constr_flesh, constr_salt, constr_x_1, constr_x_2],
    )
    print(x_opt)
    return x_opt


# ########## Visualisation functions ############
# Do not analyse them - they're just to hepl you.
# ###############################################


def _get_valid_manifold(
    x1s: List[float], x2s: List[float], constr: Callable
) -> List[float]:
    """Return arguments for constr for which constr(x1, x2) >= 0"""
    y = constr([x1s, x2s])
    return x1s[y >= 0], x2s[y >= 0]


def visualise_optimisation(
    objective_func: Callable,
    x_opt: Tuple[float, float],
    canvas_range: Tuple[float, float, float, float],
    constr_func: List[Callable],
):
    """Visualise optimisation of objective function acording to constraints."""

    # prepare manifold according to given ranges
    x1_range = np.linspace(canvas_range[0], canvas_range[1], num=100)
    x2_range = np.linspace(canvas_range[2], canvas_range[3], num=100)
    grid_x1, grid_x2 = np.meshgrid(x1_range, x2_range)
    obj = objective_func([grid_x1, grid_x2])

    # prepare canvas
    fig, axes = plt.subplots(nrows=1, ncols=len(constr_func), figsize=(28, 4))

    # for each constraint plot how optimal solution depend on it
    for idx in range(len(constr_func)):
        ax = axes[idx]
        constr = constr_func[idx]

        # plot curves and points
        clines = ax.contour(grid_x1, grid_x2, obj, 10, colors="black")
        ax.contourf(grid_x1, grid_x2, obj, 10, cmap="Spectral_r")
        ax.plot(
            x_opt[0],
            x_opt[1],
            "h",
            color="white",
            markeredgecolor="black",
            markersize=15,
            label="optimal solution",
        )
        x1_ok, x2_ok = _get_valid_manifold(grid_x1, grid_x2, constr)
        ax.scatter(x1_ok, x2_ok, alpha=0.05, marker=",", color="gray")

        # adjust canvas
        ax.set_ylim(*canvas_range[2:])
        ax.set_aspect("equal")
        ax.set_title(constr.__name__)
        ax.set_xlabel(r"$x_1$", fontsize=10)
        ax.set_ylabel(r"$x_2$", fontsize=10)
        ax.clabel(clines)

    # plot figure
    plt.tight_layout(pad=5)
    plt.suptitle("Solution for the problem of optimisation with constraints.")
    plt.show()


# ########## Entrypoint to the task ##############
# Run this sctipt as an entrypoint to see results
##################################################


if __name__ == "__main__":
    x_1_opt, x_2_opt = optimise()

    print("Found optimal solution:")
    print(f"\tas: x_1: {round(x_1_opt, 2)} [kg], x_2: {round(x_2_opt, 2)} [kg]")
    print(f"\tmaximised income: {round(income(x_1_opt, x_2_opt))} [zł]")

    print(f"Constraint flesh: {round(constr_flesh([x_1_opt, x_2_opt]), 2)}")
    print(f"Constraint filler: {round(constr_filler([x_1_opt, x_2_opt]), 2)}")
    print(f"Constraint salt: {round(constr_salt([x_1_opt, x_2_opt]), 2)}")

    visualise_optimisation(
        objective,
        [x_1_opt, x_2_opt],
        [-2000, 2000, -2000, 2000],
        [constr_flesh, constr_filler, constr_salt, constr_x_1, constr_x_2],
    )
