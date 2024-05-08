"""Main script for the task."""

from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class Simplex2D:
    """A class simulating 2D space simplex, i.e. a triangle."""

    def __init__(
        self,
        x_1: Tuple[float, float],
        x_2: Tuple[float, float],
        x_3: Tuple[float, float],
        objective_function: Callable,
    ) -> None:
        """
        Initialise the object.

        :param x_1: coordinates of the point from the 2D space
        :param x_2: coordinates of the point from the 2D space
        :param x_3: coordinates of the point from the 2D space
        :param objective_function: objective function to optimise
        """
        self.objective_function = objective_function
        self._x, self._y = self._sort([x_1, x_2, x_3])

    def _sort(self, points: List[Tuple[float, float]]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sort simplex elements according to the value of the objective function.

        :param points: three (X, Y) points of the simplex

        :return: simplex with elements sorted in descending order by value of objective function
        """
        func_vals = np.array([self.objective_function(func_arg) for func_arg in points])
        sorting_order = np.argsort(func_vals)
        return np.array(points)[sorting_order], func_vals[sorting_order]

    @property
    def x(self) -> np.ndarray:
        return self._x

    @x.setter
    def x(self, new_x) -> np.ndarray:
        self._x, self._y = self._sort(new_x)

    @property
    def best_point_x(self) -> np.ndarray:
        return self._x[0]

    @property
    def best_point_y(self) -> np.ndarray:
        return self._y[0]

    @property
    def middle_point_x(self) -> np.ndarray:
        return self._x[-2]

    @property
    def middle_point_y(self) -> np.ndarray:
        return self._y[-2]

    @property
    def worst_point_x(self) -> np.ndarray:
        return self._x[-1]

    @property
    def worst_point_y(self) -> np.ndarray:
        return self._y[-1]


# ######### Implementation of Nelder-Maed algorithm ##########
# Implement functions below so that tests are able to pass.
# ############################################################


def rosenbrock_function(x: np.ndarray) -> float:
    """
    Rosenbrock function implementation.

    :param x: input parameters vector

    :return: value of bird function for given input
    """
    x1, x2 = x
    return (1 - x1) ** 2 + 100 * (x2 - x1**2) ** 2


def get_centroid(x_1: np.ndarray, x_2: np.ndarray) -> np.ndarray:
    """
    Get coordinates of the centroid computed from simplex points.

    :param simplex_x: three points of the 2D space
    :return: coordinates of the centroid
    """
    return (x_1 + x_2) / 2


def reflect(point: np.ndarray, centroid: np.ndarray, alpha: float) -> np.ndarray:
    """
    Reflect the worst point through the centroid of the remaining points.

    :param point: the worst point to reflect
    :param centroid: centroid of a simplex
    :param alpha: reflection scale

    :return: reflected point
    """
    if alpha <= 0:
        raise ValueError(
            "Invalid value of alpha parameter. Alpha must be greater than 0!"
        )
    return centroid + alpha * (centroid - point)


def expand(point: np.ndarray, centroid: np.ndarray, gamma: float) -> np.ndarray:
    """
    Expand the reflected point.

    :param point: reflected point
    :param centroid: centroid of a simplex
    :param gamma: expansion scale

    :return: expanded point
    """
    if gamma <= 1:
        raise ValueError(
            "Invalid value of gamma parameter. Gamma must be greater than 1!"
        )

    return centroid + gamma * (point - centroid)


def contract(point: np.ndarray, centroid: np.ndarray, beta: float) -> np.ndarray:
    """
    Contract the worst point towards the centroid.

    :param point: point to contract
    :param centroid: centroid of a simplex
    :param beta: scale of contraction

    :return: contracted point
    """
    if beta <= 0 or beta >= 1:
        raise ValueError(
            "Invalid value of beta parameter. Beta must be in range (0,1)!"
        )

    return centroid + beta * (point - centroid)


def shrink(simplex: np.ndarray, sigma: float) -> np.ndarray:
    """
    Reduce the simplex towards the best point.

    :param simplex: simplex with candidate points
    :param sigma: scale of shrink

    :return: simplex with all point but the best shrinked towards it
    """

    if sigma <= 0 or sigma >= 1:
        raise ValueError(
            "Invalid value of sigma parameter. Sigma must be in range (0,1)!"
        )

    best_point = simplex[0]

    return np.array([best_point + sigma * (point - best_point) for point in simplex])


def run_nelder_mead(
    simplex: Simplex2D,
    alpha: float = 1.0,
    gamma: float = 2.0,
    beta: float = 0.5,
    sigma: float = 0.5,
    max_iter: int = 1000,
) -> List[np.ndarray]:
    """
    Runs Nelder-Mead algorithm for optimization. Simplex2D class allows convenient parameters access and handles vertices sorting.

    :param simplex: initial simplex
    :param objective_function: function to minimize
    :param alpha: reflection scale, defaults to 1.
    :param gamma: expansion scale, defaults to 2.
    :param beta: contraction scale, defaults to 0.5
    :param sigma: shrink scale, defaults to 0.5
    :param max_iter: max number of process iteration, defaults to 1000

    :return: the best point found in the optimization process and simplex history
    """
    # Order vertices w.r.p. their function values
    simplex_history = [simplex.x]

    for _ in range(max_iter):
        print(f"Current simplex coords: {simplex.x.tolist()}")

        # Calculate centroid (all points except worst one)
        # and reference points from the simplex - best, 2nd best, worst
        centroid = get_centroid(x_1=simplex.best_point_x, x_2=simplex.middle_point_x)

        # Reflect the worst point about the centroid and evaluate with the objective function
        reflected_point_x = reflect(simplex.worst_point_x, centroid, alpha)
        reflected_point_y = simplex.objective_function(reflected_point_x)

        # Reflected point is better than 2nd worst point
        if reflected_point_y < simplex.middle_point_y:
            if reflected_point_y < simplex.best_point_y:
                # If the reflection gives a better result than the current best,
                # try an expansion in that direction.
                expanded_point_x = expand(reflected_point_x, centroid, gamma)
                expanded_point_y = simplex.objective_function(expanded_point_x)
                # Replace the worst point with the better one from {expanded, reflected}
                if expanded_point_y < reflected_point_y:
                    simplex.x = [
                        simplex.best_point_x,
                        simplex.middle_point_x,
                        expanded_point_x,
                    ]
                else:
                    simplex.x = [
                        simplex.best_point_x,
                        simplex.middle_point_x,
                        reflected_point_x,
                    ]
            else:
                # If reflected point is better than 2nd worst but not than the best -
                # replace the worst simplex point
                simplex.x = [
                    simplex.best_point_x,
                    simplex.middle_point_x,
                    reflected_point_x,
                ]
        else:
            # Compute contraction using the worse of {reflected, worst simplex point}
            if reflected_point_y < simplex.worst_point_y:
                contracted_point = contract(reflected_point_x, centroid, beta)
            else:
                contracted_point = contract(simplex.worst_point_x, centroid, beta)
            contracted_point_value = simplex.objective_function(contracted_point)
            # If contraction helps - replace the worst point; oth. shrink towards best point
            if contracted_point_value < simplex.worst_point_y:
                simplex.x = [
                    simplex.best_point_x,
                    simplex.middle_point_x,
                    contracted_point,
                ]
            else:
                # Shrinking replaces all points except the best one
                simplex.x = shrink(simplex.x, sigma)

        # Re-sort simplex w.r.p. their function values
        simplex_history.append(simplex.x)

    optimal_point = simplex_history[-1][0]
    return optimal_point, simplex_history


# ########## Visualisation functions ############
# Do not analyse them - they're just to help you.
# ###############################################


def get_canvas_range(
    simplex_history: List[np.ndarray], padding: float = 2
) -> np.ndarray:
    reshaped_points = np.array(simplex_history).reshape(-1, 2)
    min_x = min(reshaped_points[:, 0]) - padding
    max_x = max(reshaped_points[:, 0]) + padding
    min_y = min(reshaped_points[:, 1]) - padding
    max_y = max(reshaped_points[:, 1]) + padding
    return np.array([min_x, max_x, min_y, max_y])


def visualise_nelder_mead_optimisation(
    simplex_history: List[np.ndarray],
    objective_func: Callable,
    canvas_range: Tuple[float, float, float, float],
):
    """Visualise optimisation of an objective function with Nelder-Mead algorithm."""

    # Convert points in simplex history from nupny arrays to tuples
    simplex_history = [
        [tuple(point) for point in simplex] for simplex in simplex_history
    ]

    # Extract simplex history elements
    initial_simplex = simplex_history[0]
    final_simplex = simplex_history[-1]
    optimal_point = final_simplex[0]

    # Prepare manifold according to given ranges
    x1_range = np.linspace(canvas_range[0], canvas_range[1], num=1000)
    x2_range = np.linspace(canvas_range[2], canvas_range[3], num=1000)
    grid_x1, grid_x2 = np.meshgrid(x1_range, x2_range)
    obj = objective_func([grid_x1, grid_x2])

    # Prepare canvas
    fig, ax = plt.subplots(figsize=(8, 8))
    cplot = ax.contourf(grid_x1, grid_x2, obj, 10, cmap="Spectral_r", alpha=1)
    clines = ax.contour(grid_x1, grid_x2, obj, 10, colors="black")

    # Set of already plotted points
    visited_points = set()

    # Draw initial simplex
    for point in initial_simplex:
        ax.plot(
            point[0],
            point[1],
            "d",
            color="gray",
            markeredgecolor="black",
            markersize=7,
            alpha=1.0,
        )
        visited_points.add(point)

    # Draw final simplex
    for point in final_simplex:
        ax.plot(
            point[0],
            point[1],
            "o",
            color="white",
            markeredgecolor="black",
            markersize=10,
            alpha=0.7,
        )
        visited_points.add(point)

    # Draw optimum
    ax.plot(
        optimal_point[0],
        optimal_point[1],
        "h",
        color="white",
        markeredgecolor="black",
        markersize=12,
    )
    visited_points.add(optimal_point)

    # Draw all intermediate points in simplex history
    for simplex in simplex_history[1:-1]:
        for point in simplex:
            if point not in visited_points:
                ax.plot(
                    point[0],
                    point[1],
                    "o",
                    color="gray",
                    markeredgecolor="black",
                    markersize=7,
                    alpha=0.7,
                )
                visited_points.add(point)

    # Draw lines between simplex points
    for i, simplex in enumerate(simplex_history):
        point_pairs = zip(simplex, np.roll(simplex, -1, axis=0))
        for p1, p2 in point_pairs:
            alpha = 0.1 + 0.9 * (i / len(simplex_history))
            ax.plot(
                (p1[0], p2[0]),
                (p1[1], p2[1]),
                color="white",
                linewidth=0.7,
                alpha=alpha,
            )

    # Adjust canvas
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x_1$", fontsize=16)
    ax.set_ylabel(r"$x_2$", fontsize=16)
    ax.clabel(clines)

    # Plot figure
    plt.tight_layout(pad=5)
    plt.suptitle("Process of optimization using Nelder-Mead algorithm.")
    plt.show()


# ########## Entrypoint to the task ##############
# Run this script as an entrypoint to see results
##################################################

if __name__ == "__main__":
    # initialise variables and parameters of the optimisation
    objective_function = rosenbrock_function
    initial_x_1 = [-1.5, -1.5]
    initial_x_2 = [-1.0, -1.5]
    initial_x_3 = [-1.5, 0.0]
    alpha = 1.0
    gamma = 2.0
    beta = 0.5
    sigma = 0.5
    max_iter = 10

    # preform optimisation
    simplex = Simplex2D(
        x_1=initial_x_1,
        x_2=initial_x_2,
        x_3=initial_x_3,
        objective_function=objective_function,
    )
    optimal_point, simplex_history = run_nelder_mead(
        simplex=simplex,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        sigma=sigma,
        max_iter=max_iter,
    )
    optimal_point_val = objective_function(optimal_point)
    canvas_range = get_canvas_range(simplex_history)
    print(canvas_range)

    # visualise optimisation
    print("Found optimal solution:")
    print(f"\tas: x_1: {round(optimal_point[0], 4)}, x_2: {round(optimal_point[1], 4)}")
    print(
        f"\tobjective function value at identified point: {round(optimal_point_val, 4)}"
    )
    visualise_nelder_mead_optimisation(
        simplex_history, objective_function, canvas_range
    )
