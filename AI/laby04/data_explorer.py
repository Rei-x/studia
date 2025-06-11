import os
import matplotlib.pyplot as plt
import seaborn as sns


def run_exploration(df, output_dir):
    print("\n--- 1. EKSPLORACJA DANYCH ---")

    print("\n[INFO] Podstawowe informacje o zbiorze:")
    df.info()

    print("\n[INFO] Statystyki opisowe:")
    print(df.describe().T)

    print("\n[INFO] Liczba brakujących wartości:")
    print(df.isnull().sum())

    plt.figure(figsize=(12, 7))
    sns.countplot(
        x="CLASS", data=df, palette="viridis", order=df["CLASS"].value_counts().index
    )
    plt.title("Rozkład klas (etykiet) w zbiorze danych", fontsize=16)
    plt.xlabel("Klasa", fontsize=12)
    plt.ylabel("Liczba próbek", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "class_distribution.png"))
    plt.close()
    print(
        f"\n[OK] Zapisano wykres rozkładu klas w '{output_dir}class_distribution.png'"
    )

    features = df.drop("CLASS", axis=1)
    features.hist(bins=30, figsize=(20, 15), layout=(6, 4), color="darkcyan")
    plt.suptitle("Rozkłady wartości dla poszczególnych cech", size=22, y=1.03)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "feature_histograms.png"))
    plt.close()
    print(f"[OK] Zapisano histogramy cech w '{output_dir}feature_histograms.png'")
