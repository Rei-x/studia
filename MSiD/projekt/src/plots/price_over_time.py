import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.get_data import get_parsed_data


def price_over_time():
    df = get_parsed_data()
    df["createdAt"] = pd.to_datetime(df["createdAt"])

    df.sort_values("createdAt", inplace=True)

    rolling_window = 1000
    df["smoothed_price"] = (
        df["price"].rolling(window=rolling_window, center=True).mean()
    )

    plt.figure(figsize=(20, 10))
    ax = sns.lineplot(x="createdAt", y="smoothed_price", data=df, color="blue")

    ax.set_title("Rolling Average Price over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    plt.grid(True)

    plt.savefig("docs/plots/price_over_time.png")


if __name__ == "__main__":
    price_over_time()
