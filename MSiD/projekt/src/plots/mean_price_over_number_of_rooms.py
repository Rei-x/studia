import matplotlib.pyplot as plt
import seaborn as sns

from src.get_data import get_parsed_data


def mean_price_over_number_of_rooms():
    filtered = get_parsed_data()

    plt.figure(figsize=(12, 10))

    ax = sns.barplot(
        x="numberOfRooms",
        y="price",
        data=filtered,
        errorbar="sd",
        err_kws={"linewidth": 2},
    )
    ax.bar_label(ax.containers[0])  # type: ignore
    ax.set_title("Średnia cena mieszkania w zależności od liczby pokoi")
    ax.set_xlabel("Liczba pokoi")
    ax.set_ylabel("Cena")
    price_per_room = filtered.copy()
    price_per_room["pricePerRoom"] = (
        price_per_room["price"] / price_per_room["numberOfRooms"]
    )

    plt.grid(True)

    plt.savefig("docs/plots/mean_price_over_number_of_rooms.png")


if __name__ == "__main__":
    mean_price_over_number_of_rooms()
