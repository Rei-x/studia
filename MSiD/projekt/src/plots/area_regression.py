from src.get_data import get_parsed_data
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def area_regression():
    df = get_parsed_data()
    regression_area = LinearRegression().fit(df[["area"]], df["price"])

    # Calculate Pearson correlation coefficient
    correlation_matrix = np.corrcoef(df["area"], df["price"])
    pearson_corr = correlation_matrix[0, 1]

    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        x="area",
        y="price",
        data=df,
        color="blue",
        s=100,
        edgecolor="black",
        alpha=0.6,
    )
    plt.plot(
        df["area"],
        regression_area.predict(df[["area"]]),
        color="red",
        linewidth=2,
    )
    plt.title("Cena od powierzchni")
    plt.xlabel("Powierzchnia [m^2]")
    plt.ylabel("Cena [zł]")

    plt.annotate(
        f"Pearson r: {pearson_corr:.2f}",
        xy=(0.05, 0.95),
        xycoords="axes fraction",
        fontsize=12,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round", fc="white", ec="gray"),
    )

    plt.grid(True)
    plt.savefig("docs/plots/area_regression.png")


if __name__ == "__main__":
    area_regression()
