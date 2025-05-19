import pandas as pd
import os

# Load the data files
data_path = "./data"
marketing_leads_file = os.path.join(
    data_path, "olist_marketing_qualified_leads_dataset.csv"
)
closed_deals_file = os.path.join(data_path, "olist_closed_deals_dataset.csv")

try:
    # Load data
    marketing_leads = pd.read_csv(marketing_leads_file)
    closed_deals = pd.read_csv(closed_deals_file)

    # Print basic info about datasets
    print("Dataset: olist_marketing_qualified_leads_dataset.csv")
    print(f"Rows: {marketing_leads.shape[0]}, Columns: {marketing_leads.shape[1]}")
    print()

    print("Dataset: olist_closed_deals_dataset.csv")
    print(f"Rows: {closed_deals.shape[0]}, Columns: {closed_deals.shape[1]}")
    print()

    # Convert date columns
    try:
        marketing_leads["first_contact_date"] = pd.to_datetime(
            marketing_leads["first_contact_date"], errors="coerce"
        )
        closed_deals["won_date"] = pd.to_datetime(
            closed_deals["won_date"], errors="coerce"
        )
    except:
        pass

    # Start index from where the provided table left off
    start_index = 46

    # Function to generate column profile in the desired format
    def profile_column(df, df_name, column_name, index):
        col = df[column_name]
        dtype = col.dtype

        # Determine number of unique values
        unique_count = col.nunique()

        # Determine value range based on data type
        if pd.api.types.is_numeric_dtype(dtype) and not pd.api.types.is_bool_dtype(
            dtype
        ):
            if unique_count > 10:
                value_range = f"{col.min()} - {col.max()}"
            else:
                unique_vals = sorted(col.dropna().unique())
                value_range = f"{unique_count} unikalnych wartości ({', '.join(map(str, unique_vals))})"
        elif pd.api.types.is_datetime64_dtype(dtype):
            value_range = (
                f"{col.min().strftime('%Y-%m-%d')} - {col.max().strftime('%Y-%m-%d')}"
            )
        else:
            if unique_count <= 8:
                unique_vals = [str(val) for val in sorted(col.dropna().unique())]
                value_range = (
                    f"{unique_count} unikalnych wartości ({', '.join(unique_vals)})"
                )
            else:
                value_range = f"{unique_count} unikalnych wartości"

        # Check for missing values
        missing_count = col.isna().sum()
        missing_pct = (missing_count / len(col)) * 100

        # Generate notes on data quality
        if missing_count > 0:
            notes = f"{missing_count} brakujących wartości ({missing_pct:.1f}%)"
        else:
            notes = "Kompletne dane"

        # Add additional context based on column name
        if "id" in column_name.lower() and unique_count == len(df):
            notes += ", klucz główny"
        elif column_name == "mql_id":
            notes += ", klucz obcy do tabeli potencjalnych klientów"
        elif column_name == "seller_id":
            notes += ", klucz obcy do tabeli sprzedawców"
        elif column_name == "sdr_id" or column_name == "sr_id":
            notes += ", identyfikator przedstawiciela handlowego"
        elif "id" in column_name.lower():
            notes += ", identyfikator"

        if pd.api.types.is_datetime64_dtype(dtype):
            notes += ", data w formacie datetime"
        elif "date" in column_name.lower() and not pd.api.types.is_datetime64_dtype(
            dtype
        ):
            notes += ", wymaga konwersji na format daty"

        # Add column-specific descriptions
        column_descriptions = {
            "origin": "źródło pozyskania potencjalnego klienta",
            "landing_page_id": "identyfikator strony docelowej",
            "first_contact_date": "data pierwszego kontaktu",
            "business_segment": "segment biznesowy klienta",
            "lead_type": "typ potencjalnego klienta",
            "lead_behaviour_profile": "profil zachowania klienta",
            "has_company": "czy klient posiada firmę",
            "has_gtin": "czy produkty mają kody GTIN",
            "business_type": "typ działalności biznesowej",
            "average_stock": "średni stan magazynowy",
            "declared_product_catalog_size": "deklarowana liczba produktów w katalogu",
            "declared_monthly_revenue": "deklarowany miesięczny przychód",
            "sdr_id": "identyfikator przedstawiciela sprzedaży",
            "sr_id": "identyfikator kierownika sprzedaży",
            "won_date": "data finalizacji sprzedaży",
        }

        if column_name in column_descriptions:
            notes += f", {column_descriptions[column_name]}"

        return {
            "Lp.": index,
            "Atrybut": f"{df_name}.{column_name}",
            "Typ danych": dtype,
            "Zakres wartości": value_range,
            "Uwagi – ocena jakości danych": notes,
        }

    # Profile all columns and print in table format
    all_profiles = []

    # Profile marketing_leads columns
    df_name = "olist_marketing_qualified_leads_dataset"
    for col_name in marketing_leads.columns:
        all_profiles.append(
            profile_column(marketing_leads, df_name, col_name, start_index)
        )
        start_index += 1

    # Profile closed_deals columns
    df_name = "olist_closed_deals_dataset"
    for col_name in closed_deals.columns:
        all_profiles.append(
            profile_column(closed_deals, df_name, col_name, start_index)
        )
        start_index += 1

    # Print profiles in table format
    for profile in all_profiles:
        print(f"{profile['Lp.']}")
        print(f"{profile['Atrybut']}")
        print(f"{profile['Typ danych']}")
        print(f"{profile['Zakres wartości']}")
        print(f"{profile['Uwagi – ocena jakości danych']}")
        print()

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback

    traceback.print_exc()
