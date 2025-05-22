# olist_etl/assets/raw_data_assets.py

import pandas as pd
from dagster import asset
import kagglehub
import os  # For joining paths


# --- Downloader Assets (as you provided) ---
@asset(group_name="downloaders", compute_kind="path")
def olist_ecommerce_dataset_path() -> str:
    """
    Downloads the Olist Brazilian E-Commerce dataset using kagglehub
    and returns the local path to the downloaded files.
    """
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    # kagglehub.dataset_download returns the path to the directory containing the files
    return str(path)  # Ensure it's a string


@asset(group_name="downloaders", compute_kind="path")
def olist_marketing_dataset_path() -> str:
    """
    Downloads the Olist Marketing Funnel dataset using kagglehub
    and returns the local path to the downloaded files.
    """
    path = kagglehub.dataset_download("olistbr/marketing-funnel-olist")
    return str(path)  # Ensure it's a string


# --- Assets for loading E-Commerce CSVs into Pandas DataFrames ---


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_customers_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_customers_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_customers_dataset.csv"
    )
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_geolocation_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """
    Loads the olist_geolocation_dataset.csv into a Pandas DataFrame.
    Note: This file can be large, consider specifying dtypes for optimization if needed.
    """
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_geolocation_dataset.csv"
    )
    # Example of dtype specification for potential memory optimization:
    # dtype_spec = {
    #     'geolocation_zip_code_prefix': 'int32',
    #     'geolocation_lat': 'float32',
    #     'geolocation_lng': 'float32',
    #     'geolocation_city': 'category',
    #     'geolocation_state': 'category'
    # }
    # return pd.read_csv(file_path, dtype=dtype_spec)
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_order_items_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_order_items_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_order_items_dataset.csv"
    )
    return pd.read_csv(file_path, parse_dates=["shipping_limit_date"])


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_order_payments_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_order_payments_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_order_payments_dataset.csv"
    )
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_order_reviews_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_order_reviews_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_order_reviews_dataset.csv"
    )
    # Dates in reviews might need parsing if you use them directly as dates
    date_cols = ["review_creation_date", "review_answer_timestamp"]
    return pd.read_csv(file_path, parse_dates=date_cols)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_orders_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_orders_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(olist_ecommerce_dataset_path, "olist_orders_dataset.csv")
    # Parse all potential date columns
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    return pd.read_csv(file_path, parse_dates=date_cols)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_products_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_products_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(olist_ecommerce_dataset_path, "olist_products_dataset.csv")
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_sellers_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_sellers_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(olist_ecommerce_dataset_path, "olist_sellers_dataset.csv")
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_product_category_name_translation_df(
    olist_ecommerce_dataset_path: str,
) -> pd.DataFrame:
    """Loads the product_category_name_translation.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "product_category_name_translation.csv"
    )
    return pd.read_csv(file_path)


# --- Assets for loading Marketing Funnel CSVs into Pandas DataFrames ---


@asset(group_name="raw_data_marketing", compute_kind="pandas")
def raw_closed_deals_df(olist_marketing_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_closed_deals_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_marketing_dataset_path, "olist_closed_deals_dataset.csv"
    )
    return pd.read_csv(
        file_path, parse_dates=["won_date"]
    )  # 'won_date' looks like a date


@asset(group_name="raw_data_marketing", compute_kind="pandas")
def raw_marketing_qualified_leads_df(olist_marketing_dataset_path: str) -> pd.DataFrame:
    """Loads the olist_marketing_qualified_leads_dataset.csv into a Pandas DataFrame."""
    file_path = os.path.join(
        olist_marketing_dataset_path, "olist_marketing_qualified_leads_dataset.csv"
    )
    return pd.read_csv(file_path, parse_dates=["first_contact_date"])
