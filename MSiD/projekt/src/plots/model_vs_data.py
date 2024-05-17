from sklearn.linear_model import LogisticRegression
from src import model
from src.get_data import get_parsed_data
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def model_vs_data():
    df = get_parsed_data()
    margins = [300, 500, 700, 1000]
    plt.figure(figsize=(20, 12))  # Adjust the figure size as needed

    for i, margin in enumerate(margins, start=1):
        good_deals = df.apply(
            lambda row: model.is_occasional_rental(
                row["price"], row["area"], margin=margin
            ),
            axis=1,
        )

        good_deals_df = df[good_deals]
        not_good_deals_df = df[~good_deals]

        # Calculate the percentage of good deals
        percentage_good_deals = 100 * good_deals.mean()

        X = df[["area", "price"]]
        y = good_deals.astype(int)
        log_reg = LogisticRegression()
        log_reg.fit(X, y)

        plt.subplot(2, 2, i)  # Configuring the subplot grid
        sns.scatterplot(
            x="area",
            y="price",
            data=not_good_deals_df,
            color="red",
            label="Normalne oferty",
            s=50,
        )
        sns.scatterplot(
            x="area", y="price", data=good_deals_df, color="green", label="Okazje", s=50
        )

        x_values = np.linspace(df["area"].min(), df["area"].max(), 300)
        y_values = (
            -(log_reg.coef_[0][0] * x_values + log_reg.intercept_[0])
            / log_reg.coef_[0][1]
        )
        plt.plot(x_values, y_values, color="blue", label="Granica decyzyjna")

        plt.xlabel("Powierzchnia [m^2]")
        plt.ylabel("Cena [zł]")
        plt.title(
            f"Wyniki modelu dla marginesu {margin} zł ({percentage_good_deals:.2f}% okazji)"
        )
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.savefig("docs/plots/multi_model_vs_data.png")


if __name__ == "__main__":
    model_vs_data()
