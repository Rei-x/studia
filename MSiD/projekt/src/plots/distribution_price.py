from src.get_data import get_parsed_data
import matplotlib.pyplot as plt
import seaborn as sns


def price_distribution():
    """
    This function generates a price distribution plot based on parsed data.

    Returns:
      None
    """
    df = get_parsed_data()

    plt.figure(figsize=(12, 6))

    sns.histplot(
        x="price",
        data=df,
        color="blue",
        edgecolor="black",
        alpha=0.6,
        bins=50,
    )

    plt.title("Rozkład cen")
    plt.xlabel("Cena [zł]")
    plt.ylabel("Liczba ofert")

    plt.grid(True)
    plt.savefig("docs/plots/price_distribution.png")


if __name__ == "__main__":
    price_distribution()
