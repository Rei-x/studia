from src.get_data import get_parsed_data
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns


def area_regression():
    df = get_parsed_data()
    regression_area = LinearRegression().fit(df[["area"]], df["price"])

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
    plt.ylabel(
        "Cena [zł]",
    )

    plt.grid(True)
    plt.savefig("docs/plots/area_regression.png")


if __name__ == "__main__":
    area_regression()
