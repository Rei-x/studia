"""
Fact Order Item asset for the Olist data warehouse.
"""

import pandas as pd
from dagster import (
    BackfillPolicy,
    MaterializeResult,
    asset,
    AssetExecutionContext,
)

# Import resources and dependencies
from quickstart_etl.resources.db_resource import SQLAlchemyResource
from ..schema_setup_assets import apply_foreign_keys_asset
from ...partitions import olist_monthly_partitions

# Import modular utilities
from .db_operations import delete_partition_and_append_fact_to_db
from .dimension_lookups import fetch_dimension_keys
from .data_transformations import (
    filter_orders_by_partition,
    process_delivery_days,
    process_review_scores,
    prepare_final_fact_dataframe,
    create_empty_partition_result,
)


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
) -> MaterializeResult:
    """
    Main asset for loading fact order item data.

    This asset processes order items for a specific partition, enriches them with
    dimension keys, and loads them into the fact table.
    """
    # Get partition time window
    partition_time_window = context.partition_time_window
    partition_start_dt = partition_time_window.start  # UTC-aware
    partition_end_dt = partition_time_window.end  # UTC-aware and exclusive

    context.log.info(
        f"Starting FactOrderItem processing for partition: {context.partition_keys} "
        f"(Window: {partition_start_dt.isoformat()} to {partition_end_dt.isoformat()})"
    )

    # Define target fact table columns
    target_fact_cols_metadata = [
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

    # Step 1: Filter orders for the current partition
    orders_partition_df = filter_orders_by_partition(
        context, raw_orders_df, partition_start_dt, partition_end_dt
    )

    if orders_partition_df.empty:
        context.log.info(
            f"No orders found for partition {context.partition_keys}. Skipping fact load."
        )
        return create_empty_partition_result(
            context,
            target_fact_cols_metadata,
            partition_start_dt,
            partition_end_dt,
            "No data in partition",
        )

    context.log.info(
        f"Found {len(orders_partition_df)} orders for partition {context.partition_keys}."
    )

    # Step 2: Filter order items based on partition orders
    fact_df = pd.merge(
        raw_order_items_df,
        orders_partition_df[["order_id"]],
        on="order_id",
        how="inner",
    )

    if fact_df.empty:
        context.log.info(
            f"No order items for partition {context.partition_keys} after merge."
        )
        return create_empty_partition_result(
            context,
            target_fact_cols_metadata,
            partition_start_dt,
            partition_end_dt,
            "No order items in partition",
        )

    context.log.info(
        f"Processing {len(fact_df)} order items for partition {context.partition_keys}."
    )

    # Step 3: Merge additional order information
    fact_df = pd.merge(
        fact_df,
        orders_partition_df[
            [
                "order_id",
                "customer_id",
                "order_purchase_timestamp",
                "order_delivered_customer_date",  # Add this column
            ]
        ],
        on="order_id",
        how="left",
    )

    # Step 4: Fetch dimension keys
    engine = sql_alchemy_resource.get_engine()
    schema_name = "olist"

    try:
        fact_df = fetch_dimension_keys(context, engine, fact_df, schema_name)
    except Exception as e:
        context.log.error(f"Error during dimension key lookup: {e}")
        raise

    # Step 5: Process review scores
    fact_df = process_review_scores(orders_partition_df, raw_order_reviews_df, fact_df)

    # Process delivery days
    fact_df = process_delivery_days(orders_partition_df, fact_df)

    # Step 6: Prepare final fact DataFrame
    final_fact_df = prepare_final_fact_dataframe(
        context, fact_df, target_fact_cols_metadata
    )

    if final_fact_df.empty:
        context.log.info(
            f"No valid fact rows remain after FK checks for partition {context.partition_keys}."
        )
        return create_empty_partition_result(
            context,
            target_fact_cols_metadata,
            partition_start_dt,
            partition_end_dt,
            "No valid rows after FK checks",
        )

    # Step 7: Load data to database
    return delete_partition_and_append_fact_to_db(
        context,
        engine,
        final_fact_df,
        "FACT_ORDER_ITEM",
        schema_name,
        target_fact_cols_metadata,
        pd.Timestamp(partition_start_dt),
        pd.Timestamp(partition_end_dt),
    )
