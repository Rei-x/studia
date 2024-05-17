import pandas as pd
import matplotlib.pyplot as plt

from src.get_data import get_parsed_data


def assign_group(x):
    base = x.min()
    groups = (x - base) // 5
    return groups


def difference_in_price_of_best_offers():
    df = get_parsed_data().sort_values(by="area")

    df["group"] = assign_group(df["area"])

    def average_of_cheapest_10_percent(group):
        n = max(1, int(len(group) * 0.1))  # Ensure at least one apartment is considered
        cheapest = group.nsmallest(n, "price")
        return cheapest["price"].mean()

    average_prices = df.groupby("group").apply(
        average_of_cheapest_10_percent, include_groups=False
    )

    mean_prices = df.groupby("group")["price"].mean()

    median_areas = df.groupby("group")["area"].median()

    plot_data = pd.DataFrame(
        {
            "Average of Cheapest 10%": average_prices,
            "Mean Price": mean_prices,
            "Median Area": median_areas,
        }
    )

    plot_data.sort_values(by="Median Area", inplace=True)

    plt.figure(figsize=(12, 8))
    plt.plot(
        plot_data["Median Area"],
        plot_data["Average of Cheapest 10%"],
        marker="o",
        linestyle="-",
        label="Średnia cena najtańszych 10% ofert",
    )
    plt.plot(
        plot_data["Median Area"],
        plot_data["Mean Price"],
        marker="x",
        linestyle="--",
        color="red",
        label="Średnia cena",
    )
    plt.title("Porównanie cen najtańszych 10% ofert z ceną średnią")
    plt.xlabel("Powierzchnia (±5 m^2)")
    plt.ylabel("Cena")
    plt.legend()
    plt.grid(True)
    plt.savefig("docs/plots/difference_in_price_of_best_offers.png")


if __name__ == "__main__":
    difference_in_price_of_best_offers()
