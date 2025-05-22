# olist_etl/assets/fact_assets.py

import pandas as pd
from dagster import (
    BackfillPolicy,
    MaterializeResult,
    asset,
    AssetExecutionContext,
)
from sqlalchemy import text, Engine

# Assuming your SQLAlchemyResource is correctly imported
from quickstart_etl.resources.db_resource import SQLAlchemyResource

# Import the DDL asset that applies foreign keys and creates the fact table
from .schema_setup_assets import apply_foreign_keys_asset

# Import the partitions definition
from ..partitions import olist_monthly_partitions  # Adjust path if necessary


# --- Helper function for partitioned fact load ---
def _delete_partition_and_append_fact_to_db(
    context: AssetExecutionContext,
    engine: Engine,
    final_df: pd.DataFrame,
    table_name: str,
    schema_name: str,
    target_columns_for_metadata: list[str],
    partition_start_date: pd.Timestamp,  # This will be UTC-aware
    partition_end_date: pd.Timestamp,  # This will be UTC-aware and exclusive
) -> MaterializeResult:
    rows_loaded = 0

    # For the DELETE statement, we need to ensure DIM_DATE.full_date comparison is correct.
    # If DIM_DATE.full_date is stored as a naive date, we might need to convert
    # partition_start_date and partition_end_date to naive for the SQL query parameters,
    # or ensure DIM_DATE also stores tz-aware dates (e.g., UTC).
    # For now, let's assume DIM_DATE.full_date is a DATE type and comparison with
    # timezone-aware timestamps passed as parameters will be handled correctly by the DB driver
    # (often by converting the tz-aware timestamp to the DB's session timezone or UTC before comparison).
    # It's safer if DIM_DATE also stores UTC dates if possible.
    # We'll pass the tz-aware timestamps directly to the SQL query.
    sql_partition_start_dt = partition_start_date
    sql_partition_end_exclusive_dt = partition_end_date

    try:
        with engine.connect() as connection:
            delete_statement = text(f"""
                DELETE ft
                FROM {schema_name}.{table_name} ft
                JOIN {schema_name}.DIM_DATE dd ON ft.date_key = dd.date_key
                WHERE dd.full_date >= :partition_start AND dd.full_date < :partition_end_exclusive
            """)
            result = connection.execute(
                delete_statement,
                {
                    "partition_start": sql_partition_start_dt,  # Pass tz-aware datetime
                    "partition_end_exclusive": sql_partition_end_exclusive_dt,  # Pass tz-aware datetime
                },
            )
            connection.commit()
            context.log.info(
                f"Deleted {result.rowcount} existing rows for partition {partition_start_date.strftime('%Y-%m')} "
                f"from {schema_name}.{table_name}."
            )

        if not final_df.empty:
            final_df.to_sql(
                name=table_name,
                con=engine,
                schema=schema_name,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
            context.log.info(
                f"Successfully appended {len(final_df)} rows for partition {partition_start_date.strftime('%Y-%m')} "
                f"into {schema_name}.{table_name}."
            )
            rows_loaded = len(final_df)
        else:
            context.log.info(
                f"No new data to append for partition {partition_start_date.strftime('%Y-%m')} to {schema_name}.{table_name}."
            )

        return MaterializeResult(
            metadata={
                "table": f"{schema_name}.{table_name}",
                "rows_loaded": rows_loaded,
                "operation": "delete_partition_append",
                "partition": partition_start_date.strftime("%Y-%m"),
                "num_rows": rows_loaded,
                "columns": list(final_df.columns)
                if not final_df.empty
                else target_columns_for_metadata,
                "destination_table": f"{schema_name}.{table_name}",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
                "partition_key": str(context.partition_keys),
                "partition_window_start": partition_start_date.isoformat(),
                "partition_window_end": partition_end_date.isoformat(),
            },
        )
    except Exception as e:
        context.log.error(
            f"Failed to delete/load data for partition {partition_start_date.strftime('%Y-%m')} "
            f"to {schema_name}.{table_name}: {e}"
        )
        raise


@asset(
    name="fact_order_item_loader",
    partitions_def=olist_monthly_partitions,
    deps=[apply_foreign_keys_asset],
    group_name="facts_loaders",
    key_prefix=["olist_dwh"],
    backfill_policy=BackfillPolicy.single_run(),
    compute_kind="sqlalchemy",
    description="Builds and loads a partition of the FactOrderItem table to SQL Server.",
)
def fact_order_item_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_order_items_df: pd.DataFrame,
    raw_orders_df: pd.DataFrame,
    raw_order_reviews_df: pd.DataFrame,
):
    partition_time_window = context.partition_time_window

    partition_start_dt = (
        partition_time_window.start
    )  # This is tz-aware (UTC by default from Dagster)
    partition_end_dt = partition_time_window.end  # This is tz-aware and exclusive

    context.log.info(
        f"Starting FactOrderItem processing for partition: {context.partition_keys} "
        f"(Window: {partition_start_dt.isoformat()} to {partition_end_dt.isoformat()})"
    )

    order_items_full_df = raw_order_items_df.copy()
    orders_full_df = raw_orders_df.copy()
    reviews_full_df = raw_order_reviews_df.copy()

    # --- Step 0: Filter orders_full_df for the current partition ---
    orders_full_df["order_purchase_timestamp"] = pd.to_datetime(
        orders_full_df["order_purchase_timestamp"], errors="coerce"
    )

    # ******** TIMEZONE FIX APPLIED HERE ********
    # Ensure 'order_purchase_timestamp' is UTC-aware for comparison
    if orders_full_df["order_purchase_timestamp"].dt.tz is None:
        context.log.info("Localizing naive 'order_purchase_timestamp' to UTC.")
        orders_full_df["order_purchase_timestamp"] = orders_full_df[
            "order_purchase_timestamp"
        ].dt.tz_localize("UTC")
    else:
        context.log.info("Converting 'order_purchase_timestamp' to UTC.")
        orders_full_df["order_purchase_timestamp"] = orders_full_df[
            "order_purchase_timestamp"
        ].dt.tz_convert("UTC")
    # *******************************************

    orders_partition_df = orders_full_df[
        (orders_full_df["order_purchase_timestamp"] >= partition_start_dt)
        & (orders_full_df["order_purchase_timestamp"] < partition_end_dt)
    ].copy()

    target_fact_cols_metadata = [  # Define once for empty outputs
        "order_key",
        "product_key",
        "seller_key",
        "customer_key",
        "date_key",
        "marketing_key",
        "price",
        "freight_value",
        "delivery_days",
        "review_score",
    ]

    if orders_partition_df.empty:
        context.log.info(
            f"No orders found for partition {context.partition_keys}. Skipping fact load."
        )
        return MaterializeResult(
            metadata={
                "table": "olist.FACT_ORDER_ITEM",
                "rows_loaded": 0,
                "operation": "delete_partition_append",
                "status": "No data in partition",
                "num_rows": 0,
                "columns": str(target_fact_cols_metadata),  # Convert list to string
                "destination_table": "olist.FACT_ORDER_ITEM",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
                "partition_key": str(context.partition_keys),
                "partition_window_start": partition_start_dt.isoformat(),
                "partition_window_end": partition_end_dt.isoformat(),
            },
        )
    context.log.info(
        f"Found {len(orders_partition_df)} orders for partition {context.partition_keys}."
    )

    fact_df = pd.merge(
        order_items_full_df,
        orders_partition_df[["order_id"]],
        on="order_id",
        how="inner",
    )

    if fact_df.empty:
        context.log.info(
            f"No order items for partition {context.partition_keys} after merge."
        )
        return MaterializeResult(
            metadata={
                "table": "olist.FACT_ORDER_ITEM",
                "rows_loaded": 0,
                "operation": "delete_partition_append",
                "status": "No order items in partition",
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
    context.log.info(
        f"Processing {len(fact_df)} order items for partition {context.partition_keys}."
    )

    engine = sql_alchemy_resource.get_engine()
    schema_name = "olist"

    fact_df = pd.merge(
        fact_df,
        orders_partition_df[["order_id", "customer_id", "order_purchase_timestamp"]],
        on="order_id",
        how="left",
    )

    try:
        context.log.info("Fetching dimension keys from database...")
        # 'order_purchase_timestamp' is now UTC-aware in fact_df
        fact_df["order_purchase_date_utc"] = fact_df[
            "order_purchase_timestamp"
        ].dt.normalize()  # Midnight UTC

        # For date_key_lookup (YYYYMMDD int), typically derived from a naive date.
        # If DIM_DATE.full_date is naive and date_key is based on that:
        fact_df["date_key_lookup"] = (
            fact_df["order_purchase_date_utc"]
            .dt.tz_localize(None)
            .dt.strftime("%Y%m%d")
        )

        min_date_lkp_naive = (
            fact_df["order_purchase_date_utc"].dt.tz_localize(None).min()
        )
        max_date_lkp_naive = (
            fact_df["order_purchase_date_utc"].dt.tz_localize(None).max()
        )

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

        dim_date_lkp["date_key_lookup"] = dim_date_lkp["date_key_lookup_val"].astype(
            str
        )
        fact_df = pd.merge(
            fact_df,
            dim_date_lkp[["date_key", "date_key_lookup"]],
            left_on="date_key_lookup",
            right_on="date_key_lookup",
            how="left",
        )
        fact_df.drop(columns=["date_key_lookup_val"], inplace=True, errors="ignore")

        dim_product_lkp = pd.read_sql(
            f"SELECT product_key, product_id FROM {schema_name}.DIM_PRODUCT", engine
        )
        fact_df = pd.merge(fact_df, dim_product_lkp, on="product_id", how="left")
        dim_seller_lkp = pd.read_sql(
            f"SELECT seller_key, seller_id FROM {schema_name}.DIM_SELLER", engine
        )
        fact_df = pd.merge(fact_df, dim_seller_lkp, on="seller_id", how="left")
        dim_order_lkp = pd.read_sql(
            f"SELECT order_key, order_id FROM {schema_name}.DIM_ORDER", engine
        )
        fact_df = pd.merge(fact_df, dim_order_lkp, on="order_id", how="left")
        dim_customer_lkp = pd.read_sql(
            f"SELECT customer_key, customer_id FROM {schema_name}.DIM_CUSTOMER", engine
        )
        fact_df = pd.merge(
            fact_df,
            dim_customer_lkp,
            on="customer_id",
            how="left",
            suffixes=("", "_cust"),
        )
        fact_df["marketing_key"] = pd.NA
        context.log.info("Finished fetching and merging dimension keys.")
    except Exception as e:
        context.log.error(f"Error during dimension key lookup: {e}")
        raise

    temp_delivery_dates_df = orders_partition_df[
        ["order_id", "order_estimated_delivery_date", "order_delivered_customer_date"]
    ].copy()
    for col_date in ["order_estimated_delivery_date", "order_delivered_customer_date"]:
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
    est_col = (
        "order_estimated_delivery_date_dlv_dates"
        if "order_estimated_delivery_date_dlv_dates" in fact_df.columns
        else "order_estimated_delivery_date"
    )
    del_col = (
        "order_delivered_customer_date_dlv_dates"
        if "order_delivered_customer_date_dlv_dates" in fact_df.columns
        else "order_delivered_customer_date"
    )
    fact_df["delivery_days"] = (fact_df[del_col] - fact_df[est_col]).dt.days
    fact_df["delivery_days"] = fact_df["delivery_days"].astype("Float64")

    relevant_order_ids_for_reviews = orders_partition_df["order_id"].unique()
    reviews_partition_df = reviews_full_df[
        reviews_full_df["order_id"].isin(relevant_order_ids_for_reviews)
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

    final_fact_df = pd.DataFrame(
        columns=target_fact_cols_metadata
    )  # Use pre-defined list
    for col in target_fact_cols_metadata:
        if col in fact_df.columns:
            final_fact_df[col] = fact_df[col]
        else:
            final_fact_df[col] = pd.NA

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
        context.log.info(
            f"No valid fact rows remain after FK checks for partition {context.partition_keys}."
        )
        return MaterializeResult(
            metadata={
                "num_rows": 0,
                "table": "olist.FACT_ORDER_ITEM",
                "status": "No valid rows after FK checks",
                "rows_loaded": 0,
                "operation": "delete_partition_append",
                "columns": target_fact_cols_metadata,
                "destination_table": "olist.FACT_ORDER_ITEM",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
                "partition_key": str(context.partition_keys),
                "partition_window_start": partition_start_dt.isoformat(),
                "partition_window_end": partition_end_dt.isoformat(),
            },
        )

    for col in essential_fk_cols:
        final_fact_df[col] = final_fact_df[col].astype(int)
    if "marketing_key" in final_fact_df.columns:
        final_fact_df["marketing_key"] = final_fact_df["marketing_key"].astype("Int64")
    final_fact_df["price"] = pd.to_numeric(final_fact_df["price"], errors="coerce")
    final_fact_df["freight_value"] = pd.to_numeric(
        final_fact_df["freight_value"], errors="coerce"
    )
    final_fact_df.dropna(subset=["price", "freight_value"], inplace=True)

    return _delete_partition_and_append_fact_to_db(
        context,
        engine,
        final_fact_df,
        "FACT_ORDER_ITEM",
        schema_name,
        target_fact_cols_metadata,
        pd.Timestamp(partition_start_dt),
        pd.Timestamp(partition_end_dt),
    )
