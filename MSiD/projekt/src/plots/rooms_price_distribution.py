import matplotlib.pyplot as plt
import seaborn as sns

from src.get_data import get_parsed_data


def rooms_price_distribution():
    df = get_parsed_data()
    plt.figure(figsize=(20, 10))

    number_of_bins = 20
    plt.subplot(2, 2, 1)
    sns.histplot(
        df[df["numberOfRooms"] == 1]["price"],  # type: ignore
        bins=number_of_bins,
        color="blue",
        kde=True,
    )
    plt.title("Rozkład ceny dla mieszkań 1-pokojowych")
    plt.xlabel("Cena (zł)")
    plt.ylabel("Liczba ofert")

    plt.subplot(2, 2, 2)
    sns.histplot(
        df[df["numberOfRooms"] == 2]["price"],  # type: ignore
        bins=number_of_bins,
        color="green",
        kde=True,
    )
    plt.title("Rozkład ceny dla mieszkań 2-pokojowych")
    plt.xlabel("Cena (zł)")
    plt.ylabel("Liczba ofert")

    plt.subplot(2, 2, 3)
    sns.histplot(
        df[df["numberOfRooms"] == 3]["price"],  # type: ignore
        bins=number_of_bins,
        color="red",
        kde=True,
    )
    plt.title("Rozkład ceny dla mieszkań 3-pokojowych")
    plt.xlabel("Cena (zł)")
    plt.ylabel("Liczba ofert")

    plt.subplot(2, 2, 4)
    sns.histplot(
        df[df["numberOfRooms"] == 4]["price"],  # type: ignore
        bins=number_of_bins,
        color="purple",
        kde=True,
    )
    plt.title("Rozkład ceny dla mieszkań 4-pokojowych")
    plt.xlabel("Cena (zł)")
    plt.ylabel("Liczba ofert")

    plt.tight_layout()
    plt.savefig("docs/plots/rooms_price_distribution.png")


if __name__ == "__main__":
    rooms_price_distribution()
