import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

# 1. WCZYTANIE DANYCH
print("1. WCZYTANIE DANYCH\n" + "=" * 50)
data_dir = "data/"
file_info = []
dataframes = {}


# Funkcja do obliczania rozmiaru pliku w MB
def get_file_size(file_path):
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)


# Wczytanie wszystkich plików CSV
for i, file_name in enumerate(os.listdir(data_dir)):
    if file_name.endswith(".csv"):
        file_path = os.path.join(data_dir, file_name)
        file_size = get_file_size(file_path)

        # Wczytanie danych
        df = pd.read_csv(file_path)
        dataframes[file_name] = df

        # Zapisanie informacji o pliku
        file_info.append(
            {
                "Lp.": i + 1,
                "Plik": file_name,
                "Typ": "CSV",
                "Liczba rekordów": len(df),
                "Rozmiar [MB]": file_size,
                "Opis": f"Zawiera {len(df.columns)} kolumn",
            }
        )

        print(f"Wczytano: {file_name} - {len(df)} rekordów, {file_size} MB")

# 2. ANALIZA ŹRÓDEŁ DANYCH
print("\n2. ANALIZA ŹRÓDEŁ DANYCH\n" + "=" * 50)
sources_df = pd.DataFrame(file_info)
print(sources_df.to_string(index=False))

# 3. PROFILOWANIE DANYCH
print("\n3. PROFILOWANIE DANYCH\n" + "=" * 50)
profile_rows = []
attr_count = 1

# Profilowanie wszystkich atrybutów we wszystkich plikach
for file_name, df in dataframes.items():
    print(f"\nProfilowanie {file_name}...")

    for column in df.columns:
        # Określenie typu danych
        dtype = str(df[column].dtype)

        # Określenie zakresu wartości
        if pd.api.types.is_numeric_dtype(df[column]):
            if df[column].count() > 0:
                min_val = df[column].min()
                max_val = df[column].max()
                value_range = f"{min_val} - {max_val}"
            else:
                value_range = "Brak danych"
        elif dtype == "object":
            unique_vals = df[column].nunique()
            if unique_vals <= 10:
                value_range = ", ".join(
                    str(x) for x in df[column].dropna().unique()[:5]
                )
                if len(value_range) > 50:
                    value_range = value_range[:47] + "..."
            else:
                value_range = f"{unique_vals} unikalnych wartości"
        else:
            value_range = "N/A"

        # Sprawdzenie brakujących wartości
        missing = df[column].isnull().sum()
        missing_pct = (missing / len(df)) * 100

        # Notatki dot. jakości danych
        notes = []
        if missing > 0:
            notes.append(f"{missing} brakujących wartości ({missing_pct:.1f}%)")

        # Sprawdzenie potencjalnych wartości odstających
        if pd.api.types.is_numeric_dtype(df[column]) and df[column].count() > 0:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            outlier_count = (
                (df[column] < (q1 - 1.5 * iqr)) | (df[column] > (q3 + 1.5 * iqr))
            ).sum()
            if outlier_count > 0:
                outlier_pct = (outlier_count / df[column].count()) * 100
                notes.append(
                    f"{outlier_count} potencjalnych wartości odstających ({outlier_pct:.1f}%)"
                )

        # Dodanie do profilu danych
        profile_rows.append(
            {
                "Lp.": attr_count,
                "Atrybut": f"{file_name}.{column}",
                "Typ danych": dtype,
                "Zakres wartości": value_range,
                "Uwagi – ocena jakości danych": "; ".join(notes)
                if notes
                else "Dobra jakość",
            }
        )
        attr_count += 1

# Zapisanie profilu danych do ramki danych
profile_df = pd.DataFrame(profile_rows)
print(f"Profilowanie zakończone - przeanalizowano {len(profile_rows)} atrybutów")

# 4. ANALIZA ENCJI I ZWIĄZKÓW
print("\n4. ANALIZA ENCJI I ZWIĄZKÓW\n" + "=" * 50)

# Definiowanie encji na podstawie nazw plików
entities = {}
for file_name, df in dataframes.items():
    if "olist_" in file_name and "_dataset.csv" in file_name:
        entity_name = file_name.replace("olist_", "").replace("_dataset.csv", "")
        entities[entity_name] = {
            "file": file_name,
            "attributes": list(df.columns),
            "primary_key": None,
            "foreign_keys": [],
        }
    elif file_name == "product_category_name_translation.csv":
        entity_name = "product_category_translation"
        entities[entity_name] = {
            "file": file_name,
            "attributes": list(df.columns),
            "primary_key": None,
            "foreign_keys": [],
        }

# Identyfikacja kluczy głównych i obcych
for entity_name, entity_info in entities.items():
    df = dataframes[entity_info["file"]]

    # Sprawdzenie potencjalnych kluczy głównych (kolumny z unikalnymi wartościami)
    for col in df.columns:
        if col.endswith("_id") and df[col].nunique() == len(df.dropna(subset=[col])):
            entity_info["primary_key"] = col
            break

    # Jeśli nie znaleziono klucza głównego z przyrostkiem _id, szukamy innych unikalnych kolumn
    if entity_info["primary_key"] is None:
        for col in df.columns:
            if df[col].nunique() == len(df.dropna(subset=[col])):
                entity_info["primary_key"] = col
                break

# Identyfikacja relacji na podstawie wspólnych nazw kolumn
relationships = []
for entity1, info1 in entities.items():
    for entity2, info2 in entities.items():
        if entity1 != entity2:
            # Sprawdź, czy jakakolwiek kolumna w entity1 może być kluczem obcym do klucza głównego entity2
            if info2["primary_key"] is not None:
                for col in info1["attributes"]:
                    if col == info2["primary_key"] or col == f"{entity2}_id":
                        relationships.append(
                            {"from": entity1, "to": entity2, "key": col}
                        )
                        if col not in info1["foreign_keys"]:
                            info1["foreign_keys"].append(col)

# Wyświetlenie informacji o encjach
print("\nEncje:")
for entity_name, entity_info in entities.items():
    print(f"Encja: {entity_name}")
    print(f"  Klucz główny: {entity_info['primary_key']}")
    print(
        f"  Klucze obce: {', '.join(entity_info['foreign_keys']) if entity_info['foreign_keys'] else 'Brak'}"
    )
    print(f"  Atrybuty: {', '.join(entity_info['attributes'])}")
    print()

# Wyświetlenie relacji
print("\nRelacje:")
for rel in relationships:
    print(f"  {rel['from']} -> {rel['to']} (przez {rel['key']})")

# 5. ANALIZA SPRZEDAŻY I ZAMÓWIEŃ
print("\n5. ANALIZA SPRZEDAŻY I ZAMÓWIEŃ\n" + "=" * 50)

# Analiza zamówień
if "olist_orders_dataset.csv" in dataframes:
    orders_df = dataframes["olist_orders_dataset.csv"]
    print(f"\nAnaliza zamówień ({len(orders_df)} rekordów):")

    # Status zamówień
    if "order_status" in orders_df.columns:
        status_counts = orders_df["order_status"].value_counts()
        print("\nRozkład statusów zamówień:")
        for status, count in status_counts.items():
            print(f"  {status}: {count} ({count / len(orders_df) * 100:.1f}%)")

    # Analiza czasowa zamówień
    if "order_purchase_timestamp" in orders_df.columns:
        orders_df["order_purchase_timestamp"] = pd.to_datetime(
            orders_df["order_purchase_timestamp"]
        )
        orders_df["order_year_month"] = orders_df[
            "order_purchase_timestamp"
        ].dt.to_period("M")

        monthly_orders = orders_df["order_year_month"].value_counts().sort_index()
        print("\nLiczba zamówień miesięcznie (pierwsze 5 miesięcy):")
        for month, count in monthly_orders.head().items():
            print(f"  {month}: {count} zamówień")

        # Dni tygodnia
        orders_df["day_of_week"] = orders_df["order_purchase_timestamp"].dt.day_name()
        dow_orders = orders_df["day_of_week"].value_counts()
        print("\nZamówienia według dni tygodnia:")
        for day, count in dow_orders.items():
            print(f"  {day}: {count} zamówień ({count / len(orders_df) * 100:.1f}%)")

# Analiza płatności
if "olist_order_payments_dataset.csv" in dataframes:
    payments_df = dataframes["olist_order_payments_dataset.csv"]
    print(f"\nAnaliza płatności ({len(payments_df)} rekordów):")

    if "payment_type" in payments_df.columns:
        payment_counts = payments_df["payment_type"].value_counts()
        print("\nRozkład metod płatności:")
        for payment, count in payment_counts.items():
            print(f"  {payment}: {count} ({count / len(payments_df) * 100:.1f}%)")

    if "payment_value" in payments_df.columns:
        print("\nAnaliza wartości płatności:")
        print(f"  Średnia: {payments_df['payment_value'].mean():.2f}")
        print(f"  Mediana: {payments_df['payment_value'].median():.2f}")
        print(f"  Min: {payments_df['payment_value'].min():.2f}")
        print(f"  Max: {payments_df['payment_value'].max():.2f}")

        if "payment_type" in payments_df.columns:
            payment_stats = payments_df.groupby("payment_type")["payment_value"].agg(
                ["mean", "median", "min", "max", "count"]
            )
            print("\nWartość płatności według metody płatności:")
            print(payment_stats)

# Analiza produktów
if "olist_products_dataset.csv" in dataframes:
    products_df = dataframes["olist_products_dataset.csv"]
    print(f"\nAnaliza produktów ({len(products_df)} rekordów):")

    if "product_category_name" in products_df.columns:
        category_counts = products_df["product_category_name"].value_counts().head(10)
        print("\nTop 10 kategorii produktów:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} ({count / len(products_df) * 100:.1f}%)")

# Analiza klientów
if "olist_customers_dataset.csv" in dataframes:
    customers_df = dataframes["olist_customers_dataset.csv"]
    print(f"\nAnaliza klientów ({len(customers_df)} rekordów):")

    if "customer_state" in customers_df.columns:
        state_counts = customers_df["customer_state"].value_counts()
        print("\nRozkład geograficzny klientów:")
        for state, count in state_counts.head(10).items():
            print(f"  {state}: {count} ({count / len(customers_df) * 100:.1f}%)")

# 6. ANALIZA RECENZJI I SATYSFAKCJI KLIENTÓW
print("\n6. ANALIZA RECENZJI I SATYSFAKCJI KLIENTÓW\n" + "=" * 50)

if "olist_order_reviews_dataset.csv" in dataframes:
    reviews_df = dataframes["olist_order_reviews_dataset.csv"]
    print(f"\nAnaliza recenzji ({len(reviews_df)} rekordów):")

    if "review_score" in reviews_df.columns:
        score_distribution = reviews_df["review_score"].value_counts().sort_index()
        avg_score = reviews_df["review_score"].mean()

        print("\nRozkład ocen:")
        for score, count in score_distribution.items():
            print(
                f"  {score} gwiazdek: {count} recenzji ({count / len(reviews_df) * 100:.1f}%)"
            )

        print(f"\nŚrednia ocena: {avg_score:.2f} gwiazdek")

        # Analiza komentarzy
        text_cols = [col for col in reviews_df.columns if "comment" in col.lower()]
        if text_cols:
            col = text_cols[0]
            has_text = (~reviews_df[col].isnull()) & (reviews_df[col].str.strip() != "")
            reviews_with_text = has_text.sum()

            print(
                f"\nRecenzje z komentarzami: {reviews_with_text} ({reviews_with_text / len(reviews_df) * 100:.1f}%)"
            )
            print(
                f"Recenzje bez komentarzy: {len(reviews_df) - reviews_with_text} ({(len(reviews_df) - reviews_with_text) / len(reviews_df) * 100:.1f}%)"
            )
