import os
from src.get_data import get_data
import matplotlib.pyplot as plt
import seaborn as sns


def preliminary_analysis():
    if not os.path.exists("docs/plots/preliminary"):
        os.makedirs("docs/plots/preliminary")

    dataset = get_data()
    plt.figure(figsize=(10, 6))

    # price distribution

    sns.histplot(dataset["price"], bins=100, kde=True)  # type: ignore
    plt.title("Rozkład cen")
    plt.savefig("docs/plots/preliminary/price_distribution.png")

    # area distribution

    plt.figure(figsize=(10, 6))
    sns.histplot(dataset["area"], bins=100, kde=True)  # type: ignore
    plt.title("Rozkład powierzchni")
    plt.savefig("docs/plots/preliminary/area_distribution.png")

    # area and price

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="area", y="price", data=dataset)
    plt.title("Powierzchnia vs Cena")
    plt.savefig("docs/plots/preliminary/area_vs_price.png")

    # distance to city centre and price

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="distanceToCityCentre", y="price", data=dataset)
    plt.title("Dystans do centrum vs Cena")
    plt.savefig("docs/plots/preliminary/distance_vs_price.png")

    # desposit and price

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="price", y="aiDeposit", data=dataset)
    plt.title("Cena vs Kaucja")
    plt.savefig("docs/plots/preliminary/price_vs_deposit.png")

    # number of rooms and area

    plt.figure(figsize=(10, 6))
    sns.barplot(x="numberOfRooms", y="area", data=dataset)
    plt.title("Powierzchnia vs Liczba pokoi")
    plt.savefig("docs/plots/preliminary/area_vs_rooms.png")

    # number of rooms and price

    plt.figure(figsize=(10, 6))
    sns.barplot(x="numberOfRooms", y="price", data=dataset)
    plt.title("Cena vs Liczba pokoi")
    plt.savefig("docs/plots/preliminary/price_vs_rooms.png")


if __name__ == "__main__":
    preliminary_analysis()
