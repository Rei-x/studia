import matplotlib.pyplot as plt


def visualise_method(z, x1, x2, points):
    # Create a figure
    fig, ax = plt.subplots()

    # Create a contour plot
    cp = ax.contour(x1, x2, z, levels=100, cmap="viridis")

    ax.set_xlim([x1.min(), x1.max()])
    ax.set_ylim([x2.min(), x2.max()])

    # ax.plot(1, 1, 'ro')
    # Mark and connect the points (1, 1), (0.5, 0.5), and (-0.5, -0.5)

    points_T = points.T
    ax.plot(*points_T, "ro-", markersize=2)
    # ax.plot([1, 0.5, -0.5], [1, 0.5, -0.5], 'ro-')

    # Set labels
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")

    # Show the plot
    plt.show()
