import pandas as pd


def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print(f"Pomyślnie wczytano dane z '{filepath}'. Liczba wierszy: {len(df)}")
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku pod ścieżką: {filepath}")
        return None, None, None

    X = df.drop("CLASS", axis=1)
    y = df["CLASS"]

    return X, y, df
