"""
Dimension lookup utilities for fact table processing.
"""

import pandas as pd
from dagster import AssetExecutionContext
from sqlalchemy import text, Engine


def fetch_dimension_keys(
    context: AssetExecutionContext,
    engine: Engine,
    fact_df: pd.DataFrame,
    schema_name: str,
) -> pd.DataFrame:
    """
    Fetch and merge dimension keys from dimension tables.

    Args:
        context: Dagster asset execution context
        engine: SQLAlchemy engine
        fact_df: DataFrame to enrich with dimension keys
        schema_name: Database schema name

    Returns:
        DataFrame with dimension keys merged
    """
    context.log.info("Fetching dimension keys from database...")

    # Process date dimension
    fact_df = _process_date_dimension(context, engine, fact_df, schema_name)

    # Process other dimensions
    fact_df = _process_product_dimension(engine, fact_df, schema_name)
    fact_df = _process_seller_dimension(engine, fact_df, schema_name)
    fact_df = _process_order_dimension(engine, fact_df, schema_name)
    fact_df = _process_customer_dimension(engine, fact_df, schema_name)

    # Set marketing key to NA for now
    fact_df["marketing_key"] = pd.NA

    context.log.info("Finished fetching and merging dimension keys.")
    return fact_df


def _process_date_dimension(
    context: AssetExecutionContext,
    engine: Engine,
    fact_df: pd.DataFrame,
    schema_name: str,
) -> pd.DataFrame:
    """Process date dimension lookup."""
    # 'order_purchase_timestamp' is now UTC-aware in fact_df
    fact_df["order_purchase_date_utc"] = fact_df[
        "order_purchase_timestamp"
    ].dt.normalize()  # Midnight UTC

    # For date_key_lookup (YYYYMMDD int), typically derived from a naive date.
    # If DIM_DATE.full_date is naive and date_key is based on that:
    fact_df["date_key_lookup"] = (
        fact_df["order_purchase_date_utc"].dt.tz_localize(None).dt.strftime("%Y%m%d")
    )

    min_date_lkp_naive = fact_df["order_purchase_date_utc"].dt.tz_localize(None).min()
    max_date_lkp_naive = fact_df["order_purchase_date_utc"].dt.tz_localize(None).max()

    if pd.notna(min_date_lkp_naive) and pd.notna(max_date_lkp_naive):
        dim_date_lkp_query = text(f"""
            SELECT date_key, date_key AS date_key_lookup_val 
            FROM {schema_name}.DIM_DATE 
            WHERE full_date >= :min_date AND full_date <= :max_date
        """)  # Assumes DIM_DATE.full_date is a naive DATE column
        dim_date_lkp = pd.read_sql(
            dim_date_lkp_query,
            engine,
            params={
                "min_date": min_date_lkp_naive.date(),
                "max_date": max_date_lkp_naive.date(),
            },  # Pass as date objects
        )
    else:
        dim_date_lkp = pd.DataFrame(columns=["date_key", "date_key_lookup_val"])

    dim_date_lkp["date_key_lookup"] = dim_date_lkp["date_key_lookup_val"].astype(str)
    fact_df = pd.merge(
        fact_df,
        dim_date_lkp[["date_key", "date_key_lookup"]],
        left_on="date_key_lookup",
        right_on="date_key_lookup",
        how="left",
    )
    fact_df.drop(columns=["date_key_lookup_val"], inplace=True, errors="ignore")

    return fact_df


def _process_product_dimension(
    engine: Engine, fact_df: pd.DataFrame, schema_name: str
) -> pd.DataFrame:
    """Process product dimension lookup."""
    dim_product_lkp = pd.read_sql(
        f"SELECT product_key, product_id FROM {schema_name}.DIM_PRODUCT", engine
    )
    return pd.merge(fact_df, dim_product_lkp, on="product_id", how="left")


def _process_seller_dimension(
    engine: Engine, fact_df: pd.DataFrame, schema_name: str
) -> pd.DataFrame:
    """Process seller dimension lookup."""
    dim_seller_lkp = pd.read_sql(
        f"SELECT seller_key, seller_id FROM {schema_name}.DIM_SELLER", engine
    )
    return pd.merge(fact_df, dim_seller_lkp, on="seller_id", how="left")


def _process_order_dimension(
    engine: Engine, fact_df: pd.DataFrame, schema_name: str
) -> pd.DataFrame:
    """Process order dimension lookup."""
    dim_order_lkp = pd.read_sql(
        f"SELECT order_key, order_id FROM {schema_name}.DIM_ORDER", engine
    )
    return pd.merge(fact_df, dim_order_lkp, on="order_id", how="left")


def _process_customer_dimension(
    engine: Engine, fact_df: pd.DataFrame, schema_name: str
) -> pd.DataFrame:
    """Process customer dimension lookup."""
    dim_customer_lkp = pd.read_sql(
        f"SELECT customer_key, customer_id FROM {schema_name}.DIM_CUSTOMER", engine
    )
    return pd.merge(
        fact_df,
        dim_customer_lkp,
        on="customer_id",
        how="left",
        suffixes=("", "_cust"),
    )
