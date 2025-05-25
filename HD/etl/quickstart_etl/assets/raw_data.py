import pandas as pd
from dagster import asset
import kagglehub
import os


@asset(group_name="downloaders", compute_kind="path")
def olist_ecommerce_dataset_path() -> str:
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

    return str(path)


@asset(group_name="downloaders", compute_kind="path")
def olist_marketing_dataset_path() -> str:
    path = kagglehub.dataset_download("olistbr/marketing-funnel-olist")
    return str(path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_customers_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_customers_dataset.csv"
    )
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_geolocation_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_geolocation_dataset.csv"
    )

    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_order_items_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_order_items_dataset.csv"
    )
    return pd.read_csv(file_path, parse_dates=["shipping_limit_date"])


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_order_payments_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_order_payments_dataset.csv"
    )
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_order_reviews_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "olist_order_reviews_dataset.csv"
    )

    date_cols = ["review_creation_date", "review_answer_timestamp"]
    return pd.read_csv(file_path, parse_dates=date_cols)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_orders_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(olist_ecommerce_dataset_path, "olist_orders_dataset.csv")

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
    file_path = os.path.join(olist_ecommerce_dataset_path, "olist_products_dataset.csv")
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_sellers_df(olist_ecommerce_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(olist_ecommerce_dataset_path, "olist_sellers_dataset.csv")
    return pd.read_csv(file_path)


@asset(group_name="raw_data_ecommerce", compute_kind="pandas")
def raw_product_category_name_translation_df(
    olist_ecommerce_dataset_path: str,
) -> pd.DataFrame:
    file_path = os.path.join(
        olist_ecommerce_dataset_path, "product_category_name_translation.csv"
    )
    return pd.read_csv(file_path)


@asset(group_name="raw_data_marketing", compute_kind="pandas")
def raw_closed_deals_df(olist_marketing_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_marketing_dataset_path, "olist_closed_deals_dataset.csv"
    )
    return pd.read_csv(file_path, parse_dates=["won_date"])


@asset(group_name="raw_data_marketing", compute_kind="pandas")
def raw_marketing_qualified_leads_df(olist_marketing_dataset_path: str) -> pd.DataFrame:
    file_path = os.path.join(
        olist_marketing_dataset_path, "olist_marketing_qualified_leads_dataset.csv"
    )
    return pd.read_csv(file_path, parse_dates=["first_contact_date"])
