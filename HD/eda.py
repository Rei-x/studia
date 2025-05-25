# Analiza danych z Brazilian E-Commerce Public Dataset by Olist
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Ustawienia dla lepszej czytelności wykresów
plt.style.use('ggplot')
sns.set(font_scale=1.2)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# Ścieżka do folderu z danymi
data_path = 'data/'

# Wczytywanie plików CSV
def load_data():
    files = {
        'customers': 'olist_customers_dataset.csv',
        'geolocation': 'olist_geolocation_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'order_payments': 'olist_order_payments_dataset.csv',
        'order_reviews': 'olist_order_reviews_dataset.csv',
        'orders': 'olist_orders_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'category_translation': 'product_category_name_translation.csv'
    }
    
    dfs = {}
    for key, filename in files.items():
        file_path = os.path.join(data_path, filename)
        dfs[key] = pd.read_csv(file_path)
        print(f"Loaded {key}: {dfs[key].shape} rows and columns")
    
    return dfs

# Profilowanie danych - analiza jakości
def profile_data(dfs):
    for name, df in dfs.items():
        print(f"\n{'='*50}")
        print(f"Profilowanie danych: {name}")
        print(f"{'='*50}")
        
        print(f"\nLiczba rekordów: {df.shape[0]}")
        print(f"Liczba atrybutów: {df.shape[1]}")
        print(f"\nPierwsze 5 rekordów:")
        print(df.head())
        
        print("\nStatystyki:")
        print(df.describe(include='all').T)
        
        print("\nTypy danych:")
        print(df.dtypes)
        
        print("\nBrakujące wartości:")
        missing = df.isnull().sum()
        print(missing[missing > 0])
        
        print("\nUnikalne wartości dla kolumn kategorycznych:")
        for col in df.select_dtypes(include=['object']).columns:
            unique_count = df[col].nunique()
            if unique_count < 20:  # Tylko dla kolumn z małą liczbą unikalnych wartości
                print(f"{col}: {unique_count} unikalnych wartości")
                print(df[col].value_counts().head())
            else:
                print(f"{col}: {unique_count} unikalnych wartości (zbyt dużo by wyświetlić)")

# Analiza źródeł danych
def analyze_data_sources(dfs):
    print("\nAnaliza źródeł danych:")
    print(f"{'Lp.':<5}{'Plik':<35}{'Typ':<15}{'Liczba rekordów':<20}{'Rozmiar [MB]':<15}{'Opis'}")
    print(f"{'-'*90}")
    
    i = 1
    for name, df in dfs.items():
        file_path = os.path.join(data_path, files_dict[name])
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        print(f"{i:<5}{files_dict[name]:<35}{'CSV':<15}{df.shape[0]:<20}{file_size:.2f}{'MB':<15}{get_description(name)}")
        i += 1

# Opis zbiorów danych
def get_description(name):
    descriptions = {
        'customers': "Dane klientów",
        'geolocation': "Dane geolokalizacyjne",
        'order_items': "Szczegóły zamówionych przedmiotów",
        'order_payments': "Dane dotyczące płatności",
        'order_reviews': "Recenzje zamówień",
        'orders': "Zamówienia",
        'products': "Produkty",
        'sellers': "Sprzedawcy",
        'category_translation': "Tłumaczenia kategorii produktów"
    }
    return descriptions.get(name, "")

# Mapowanie nazw plików
files_dict = {
    'customers': 'olist_customers_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'order_payments': 'olist_order_payments_dataset.csv',
    'order_reviews': 'olist_order_reviews_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'category_translation': 'product_category_name_translation.csv'
}

# Główna funkcja analizy
def main():
    dfs = load_data()
    
    # Analiza źródeł danych
    analyze_data_sources(dfs)
    
    # Profilowanie danych
    # profile_data(dfs)  # Ta funkcja generuje dużo danych, więc zakomentowana
    
    # Tworzenie tabeli profilowania danych
    profile_table = []
    print("\nProfilowanie danych (analiza jakości danych oraz ich przydatności w projekcie):")
    print(f"{'Lp.':<5}{'Atrybut':<30}{'Typ danych':<15}{'Zakres wartości':<30}{'Uwagi – ocena jakości danych':<30}")
    print(f"{'-'*100}")
    
    lp = 1
    for name, df in dfs.items():
        for col in df.columns:
            data_type = str(df[col].dtype)
            
            # Określenie zakresu wartości
            if pd.api.types.is_numeric_dtype(df[col]):
                value_range = f"{df[col].min()} - {df[col].max()}"
            elif pd.api.types.is_datetime64_dtype(df[col]):
                value_range = f"{df[col].min()} - {df[col].max()}"
            else:
                unique_count = df[col].nunique()
                value_range = f"{unique_count} unikalnych wartości"
            
            # Ocena jakości
            missing_count = df[col].isnull().sum()
            quality = ""
            if missing_count > 0:
                quality = f"{missing_count} brakujących wartości ({missing_count/len(df)*100:.1f}%)"
            else:
                quality = "Kompletne dane"
                
            profile_row = {
                'Lp.': lp,
                'Atrybut': f"{name}.{col}",
                'Typ danych': data_type,
                'Zakres wartości': value_range,
                'Uwagi': quality
            }
            profile_table.append(profile_row)
            
            print(f"{lp:<5}{name}.{col:<30}{data_type:<15}{value_range:<30}{quality:<30}")
            lp += 1
    
    # Analiza związków między tabelami
    print("\nDefinicja typów encji/klas oraz związków pomiędzy nimi:")
    entity_relationships = [
        "customers - orders: one-to-many (klient może mieć wiele zamówień)",
        "orders - order_items: one-to-many (zamówienie może zawierać wiele przedmiotów)",
        "orders - order_payments: one-to-many (zamówienie może mieć wiele płatności)",
        "orders - order_reviews: one-to-one (zamówienie ma jedną recenzję)",
        "products - order_items: one-to-many (produkt może być w wielu zamówieniach)",
        "sellers - order_items: one-to-many (sprzedawca może sprzedać wiele przedmiotów)",
        "products - category_translation: many-to-one (wiele produktów może należeć do jednej kategorii)"
    ]
    
    for rel in entity_relationships:
        print(f" - {rel}")
    
    # Analiza sprzedaży według kategorii produktów
    orders = dfs['orders']
    order_items = dfs['order_items']
    products = dfs['products']
    category_translation = dfs['category_translation']
    
    # Łączenie danych
    sales_data = order_items.merge(products, on='product_id')
    sales_data = sales_data.merge(category_translation, on='product_category_name', how='left')
    
    # Analiza sprzedaży według kategorii
    category_sales = sales_data.groupby('product_category_name_english').agg({
        'order_id': 'count',
        'price': 'sum',
        'freight_value': 'sum'
    }).reset_index()
    
    category_sales.columns = ['Category', 'Number of Orders', 'Total Revenue', 'Total Freight']
    category_sales['Total Value'] = category_sales['Total Revenue'] + category_sales['Total Freight']
    category_sales = category_sales.sort_values('Total Value', ascending=False).head(10)
    
    print("\nTop 10 kategorii produktów według przychodów:")
    print(category_sales)
    
    # Analiza czasowa zamówień
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['month_year'] = orders['order_purchase_timestamp'].dt.to_period('M')
    monthly_orders = orders.groupby('month_year').size().reset_index(name='count')
    monthly_orders['month_year'] = monthly_orders['month_year'].astype(str)
    
    print("\nLiczba zamówień w czasie (miesięcznie):")
    print(monthly_orders)
    
    # Analiza geograficzna
    customers = dfs['customers']
    customer_location = customers['customer_state'].value_counts().reset_index()
    customer_location.columns = ['State', 'Number of Customers']
    
    print("\nRozkład klientów według stanu:")
    print(customer_location.head(10))
    
    # Analiza metod płatności
    payments = dfs['order_payments']
    payment_methods = payments['payment_type'].value_counts().reset_index()
    payment_methods.columns = ['Payment Method', 'Count']
    
    print("\nPopularność metod płatności:")
    print(payment_methods)
    
    # Analiza recenzji
    reviews = dfs['order_reviews']
    review_scores = reviews['review_score'].value_counts().sort_index().reset_index()
    review_scores.columns = ['Score', 'Count']
    
    print("\nRozkład ocen zamówień:")
    print(review_scores)
    
    # Propozycje zestawień wielowymiarowych
    print("\nPropozycje zestawień wielowymiarowych:")
    print("1. Sprzedaż według kategorii produktów i czasu (miesiąc/rok)")
    print("2. Sprzedaż według lokalizacji klienta (stan) i kategorii produktów")
    print("3. Średni czas dostawy według stanu klienta i kategorii produktów")
    print("4. Liczba zamówień i przychody według metody płatności i czasu")
    print("5. Oceny zamówień według kategorii produktów i sprzedawcy")
    print("6. Wartość koszyka zakupowego według stanu klienta i czasu")
    print("7. Sezonowość sprzedaży według kategorii produktów")
    print("8. Porównanie wartości zamówienia a oceny klienta")
    print("9. Analiza kosztów dostawy w zależności od odległości i wagi produktów")
    print("10. Skuteczność sprzedawców według kategorii (stosunek sprzedaży do zwrotów)")

if __name__ == "__main__":
    main()