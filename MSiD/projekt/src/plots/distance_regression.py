from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

from src.get_data import get_parsed_data


def distance_regression():
    filtered = get_parsed_data()
    regression_distance = LinearRegression().fit(
        filtered[["distanceToCityCentre"]], filtered["price"]
    )

    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        x="distanceToCityCentre",
        y="price",
        data=filtered,
        color="green",
        s=100,
        edgecolor="black",
        alpha=0.6,
    )
    plt.plot(
        filtered["distanceToCityCentre"],
        regression_distance.predict(filtered[["distanceToCityCentre"]]),
        color="red",
        linewidth=2,
    )
    plt.title("Cena mieszkania w zależności od odległości od centrum")
    plt.xlabel(
        "Odległość od centrum [m]",
    )
    plt.ylabel("Cena [zł]")

    plt.grid(True)
    plt.savefig("docs/plots/distance_regression.png")


if __name__ == "__main__":
    distance_regression()
