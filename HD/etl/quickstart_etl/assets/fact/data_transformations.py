"""
Data transformation utilities for fact table processing.
"""

import pandas as pd
from datetime import datetime
from dagster import AssetExecutionContext, MaterializeResult


def filter_orders_by_partition(
    context: AssetExecutionContext,
    orders_df: pd.DataFrame,
    partition_start_dt: datetime,
    partition_end_dt: datetime,
) -> pd.DataFrame:
    """
    Filter orders DataFrame by partition time window and handle timezone conversion.

    Args:
        context: Dagster asset execution context
        orders_df: Raw orders DataFrame
        partition_start_dt: Start of partition window (inclusive)
        partition_end_dt: End of partition window (exclusive)

    Returns:
        Filtered orders DataFrame for the partition
    """
    orders_df = orders_df.copy()

    # Convert order_purchase_timestamp to datetime
    orders_df["order_purchase_timestamp"] = pd.to_datetime(
        orders_df["order_purchase_timestamp"], errors="coerce"
    )

    # ******** TIMEZONE FIX APPLIED HERE ********
    # Ensure 'order_purchase_timestamp' is UTC-aware for comparison
    if orders_df["order_purchase_timestamp"].dt.tz is None:
        context.log.info("Localizing naive 'order_purchase_timestamp' to UTC.")
        orders_df["order_purchase_timestamp"] = orders_df[
            "order_purchase_timestamp"
        ].dt.tz_localize("UTC")
    else:
        context.log.info("Converting 'order_purchase_timestamp' to UTC.")
        orders_df["order_purchase_timestamp"] = orders_df[
            "order_purchase_timestamp"
        ].dt.tz_convert("UTC")
    # *******************************************

    orders_partition_df = orders_df[
        (orders_df["order_purchase_timestamp"] >= partition_start_dt)
        & (orders_df["order_purchase_timestamp"] < partition_end_dt)
    ].copy()

    return orders_partition_df


def process_delivery_days(
    orders_partition_df: pd.DataFrame,
    fact_df: pd.DataFrame,
) -> pd.DataFrame:
    temp_delivery_dates_df = orders_partition_df[
        ["order_id", "order_purchase_timestamp", "order_delivered_customer_date"]
    ].copy()
    for col_date in ["order_purchase_timestamp", "order_delivered_customer_date"]:
        temp_delivery_dates_df[col_date] = pd.to_datetime(
            temp_delivery_dates_df[col_date], errors="coerce"
        )
        if temp_delivery_dates_df[col_date].dt.tz is None:
            temp_delivery_dates_df[col_date] = temp_delivery_dates_df[
                col_date
            ].dt.tz_localize("UTC")
        else:
            temp_delivery_dates_df[col_date] = temp_delivery_dates_df[
                col_date
            ].dt.tz_convert("UTC")

    fact_df = pd.merge(
        fact_df,
        temp_delivery_dates_df,
        on="order_id",
        how="left",
        suffixes=("", "_dlv_dates"),
    )
    purch_column = (
        "order_purchase_timestamp_dlv_dates"
        if "order_purchase_timestamp_dlv_dates" in fact_df.columns
        else "order_purchase_timestamp"
    )
    del_col = (
        "order_delivered_customer_date_dlv_dates"
        if "order_delivered_customer_date_dlv_dates" in fact_df.columns
        else "order_delivered_customer_date"
    )
    fact_df["delivery_days"] = (fact_df[del_col] - fact_df[purch_column]).dt.days
    fact_df["delivery_days"] = fact_df["delivery_days"].astype("Float64")

    fact_df.drop(
        columns=[
            "order_purchase_timestamp_dlv_dates",
            "order_delivered_customer_date_dlv_dates",
        ],
        inplace=True,
        errors="ignore",
    )

    return fact_df


def process_review_scores(
    orders_partition_df: pd.DataFrame,
    reviews_df: pd.DataFrame,
    fact_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Process review scores and merge with fact DataFrame.

    Args:
        orders_partition_df: Filtered orders for the partition
        reviews_df: Raw reviews DataFrame
        fact_df: Fact DataFrame to enrich

    Returns:
        Fact DataFrame with review scores merged
    """
    relevant_order_ids_for_reviews = orders_partition_df["order_id"].unique()
    reviews_partition_df = reviews_df[
        reviews_df["order_id"].isin(relevant_order_ids_for_reviews)
    ]
    avg_reviews = (
        reviews_partition_df.groupby("order_id")["review_score"].mean().reset_index()
    )
    fact_df = pd.merge(
        fact_df, avg_reviews, on="order_id", how="left", suffixes=("", "_review")
    )

    if "review_score_review" in fact_df.columns:
        fact_df.rename(columns={"review_score_review": "review_score"}, inplace=True)
    elif "review_score" not in fact_df.columns:
        fact_df["review_score"] = pd.NA

    fact_df["review_score"] = fact_df["review_score"].astype("Float64")
    return fact_df


def prepare_final_fact_dataframe(
    context: AssetExecutionContext,
    fact_df: pd.DataFrame,
    target_fact_cols_metadata: list[str],
) -> pd.DataFrame:
    """
    Prepare the final fact DataFrame with proper column mapping and data types.

    Args:
        context: Dagster asset execution context
        fact_df: Processed fact DataFrame
        target_fact_cols_metadata: Expected columns for the fact table

    Returns:
        Final fact DataFrame ready for loading
    """
    # Create final DataFrame with target schema
    final_fact_df = pd.DataFrame(columns=target_fact_cols_metadata)
    for col in target_fact_cols_metadata:
        if col in fact_df.columns:
            final_fact_df[col] = fact_df[col]
        else:
            final_fact_df[col] = pd.NA

    # Handle essential foreign key validation
    essential_fk_cols = [
        "order_key",
        "product_key",
        "seller_key",
        "customer_key",
        "date_key",
    ]

    rows_before_dropna = len(final_fact_df)
    final_fact_df.dropna(subset=essential_fk_cols, inplace=True)
    rows_after_dropna = len(final_fact_df)

    if rows_before_dropna > rows_after_dropna:
        context.log.warning(
            f"Dropped {rows_before_dropna - rows_after_dropna} fact rows due to missing essential foreign keys for partition {context.partition_keys}."
        )

    if final_fact_df.empty:
        return final_fact_df

    # Convert data types
    for col in essential_fk_cols:
        final_fact_df[col] = final_fact_df[col].astype(int)

    if "marketing_key" in final_fact_df.columns:
        final_fact_df["marketing_key"] = final_fact_df["marketing_key"].astype("Int64")

    # Convert numeric columns
    final_fact_df["price"] = pd.to_numeric(final_fact_df["price"], errors="coerce")
    final_fact_df["freight_value"] = pd.to_numeric(
        final_fact_df["freight_value"], errors="coerce"
    )

    # Drop rows with missing price or freight_value
    final_fact_df.dropna(subset=["price", "freight_value"], inplace=True)

    return final_fact_df


def create_empty_partition_result(
    context: AssetExecutionContext,
    target_fact_cols_metadata: list[str],
    partition_start_dt: datetime,
    partition_end_dt: datetime,
    status: str,
) -> MaterializeResult:
    """
    Create a MaterializeResult for empty partitions.

    Args:
        context: Dagster asset execution context
        target_fact_cols_metadata: Expected columns for metadata
        partition_start_dt: Start of partition window
        partition_end_dt: End of partition window
        status: Status message for the empty result

    Returns:
        MaterializeResult with metadata for empty partition
    """
    return MaterializeResult(
        metadata={
            "table": "olist.FACT_ORDER_ITEM",
            "rows_loaded": 0,
            "operation": "delete_partition_append",
            "status": status,
            "num_rows": 0,
            "columns": target_fact_cols_metadata,
            "destination_table": "olist.FACT_ORDER_ITEM",
            "source": "olist_dwh",
            "load_time": pd.Timestamp.now().isoformat(),
            "partition_key": str(context.partition_keys),
            "partition_window_start": partition_start_dt.isoformat(),
            "partition_window_end": partition_end_dt.isoformat(),
        },
    )
