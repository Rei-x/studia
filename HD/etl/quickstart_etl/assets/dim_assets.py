# olist_etl/assets/dimension_assets.py

import pandas as pd
from dagster import (
    asset,
    Output,
    AssetExecutionContext,
    RetryPolicy,
)  # Import RetryPolicy
from sqlalchemy import text, Engine, inspect

from quickstart_etl.resources.db_resource import SQLAlchemyResource

from .schema_setup_assets import (
    create_dim_date_table_asset,
    create_dim_product_table_asset,
    create_dim_customer_table_asset,
    create_dim_seller_table_asset,
    create_dim_order_table_asset,
    create_dim_marketing_table_asset,
)

# --- Helper Functions ---


def _prepare_df_for_load(
    context: AssetExecutionContext,
    df_merged: pd.DataFrame,
    target_columns: list[str],
    business_key_column: str | None = None,
) -> pd.DataFrame:
    final_df = pd.DataFrame(columns=target_columns)
    for col in target_columns:
        if col in df_merged.columns:
            final_df[col] = df_merged[col]
        else:
            context.log.warning(
                f"Target column '{col}' not found in merged DataFrame. Filling with NA."
            )
            final_df[col] = pd.NA

    if business_key_column:
        rows_before_dropna = len(final_df)
        final_df = final_df.dropna(subset=[business_key_column])
        rows_after_dropna = len(final_df)
        if rows_before_dropna > rows_after_dropna:
            context.log.warning(
                f"Dropped {rows_before_dropna - rows_after_dropna} rows due to missing business key '{business_key_column}'."
            )
    return final_df


def _upsert_to_db_via_staging(
    context: AssetExecutionContext,
    engine: Engine,
    df_to_load: pd.DataFrame,
    target_table_name: str,
    target_schema_name: str,
    business_key_cols: list[str],
    all_target_cols_for_df: list[str],
) -> Output[dict]:
    if df_to_load.empty:
        context.log.info(
            f"No data to upsert into {target_schema_name}.{target_table_name}."
        )
        return Output(
            value={
                "table": f"{target_schema_name}.{target_table_name}",
                "rows_inserted": 0,
                "rows_updated": 0,
                "operation": "upsert_skipped_empty_df",
            },
            metadata={
                "num_rows_processed_in_df": 0,
                "columns": all_target_cols_for_df,
                "destination_table": f"{target_schema_name}.{target_table_name}",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
            },
        )

    # More unique staging table name to minimize potential clashes if runs overlap slightly
    # and cleanup fails, though concurrency control is the primary fix for deadlocks.
    run_id_prefix = context.run_id.split("-")[0]  # Short prefix from run_id
    staging_table_name = f"stg_{target_table_name}_{run_id_prefix}_{pd.Timestamp.now().strftime('%H%M%S%f')}".lower()

    rows_affected_by_merge = 0

    try:
        with engine.connect() as connection:
            # Check if staging table exists and drop it explicitly first to reduce to_sql's internal reflection work
            # This is a small optimization, the main fix is concurrency control.
            inspector = inspect(connection)
            if inspector.has_table(staging_table_name, schema=target_schema_name):
                context.log.info(
                    f"Dropping existing staging table {target_schema_name}.{staging_table_name}"
                )
                connection.execute(
                    text(f"DROP TABLE {target_schema_name}.{staging_table_name}")
                )
                # No commit needed for DROP TABLE usually, or it's part of the transaction

            df_to_load.to_sql(
                name=staging_table_name,
                con=connection,
                schema=target_schema_name,
                index=False,
                chunksize=1000,
            )
            context.log.info(
                f"Loaded {len(df_to_load)} rows into staging table {target_schema_name}.{staging_table_name}."
            )

            update_set_clauses = [
                f"Target.{col} = Source.{col}"
                for col in all_target_cols_for_df
                if col not in business_key_cols
            ]
            insert_cols_target = ", ".join(all_target_cols_for_df)
            insert_cols_source = ", ".join(
                [f"Source.{col}" for col in all_target_cols_for_df]
            )
            join_conditions = " AND ".join(
                [f"Target.{bk} = Source.{bk}" for bk in business_key_cols]
            )

            simple_merge_sql = f"""
            MERGE {target_schema_name}.{target_table_name} AS Target
            USING {target_schema_name}.{staging_table_name} AS Source
            ON ({join_conditions})
            WHEN MATCHED THEN
                UPDATE SET {", ".join(update_set_clauses)}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insert_cols_target})
                VALUES ({insert_cols_source});
            """

            result = connection.execute(text(simple_merge_sql))
            rows_affected_by_merge = result.rowcount if result else 0
            context.log.info(
                f"Successfully executed MERGE into {target_schema_name}.{target_table_name}. Affected rows: {rows_affected_by_merge}"
            )

            connection.execute(
                text(f"DROP TABLE {target_schema_name}.{staging_table_name}")
            )
            connection.commit()  # Commit all operations: staging load, merge, staging drop
            context.log.info(
                f"Dropped staging table {target_schema_name}.{staging_table_name} and committed transaction."
            )

        return Output(
            value={
                "table": f"{target_schema_name}.{target_table_name}",
                "rows_affected_by_merge": rows_affected_by_merge,
                "operation": "upsert_via_staging",
            },
            metadata={
                "num_rows_processed_in_df": len(df_to_load),
                "columns": all_target_cols_for_df,
                "destination_table": f"{target_schema_name}.{target_table_name}",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
            },
        )
    except Exception as e:
        context.log.error(
            f"Failed to upsert data to {target_schema_name}.{target_table_name}: {e}"
        )
        # Attempt to drop staging table on error if it exists (outside the transaction that might have rolled back)
        try:
            with engine.connect() as conn_cleanup:  # New connection for cleanup
                inspector = inspect(conn_cleanup)
                if inspector.has_table(staging_table_name, schema=target_schema_name):
                    conn_cleanup.execute(
                        text(f"DROP TABLE {target_schema_name}.{staging_table_name}")
                    )
                    conn_cleanup.commit()
                    context.log.info(
                        f"Cleaned up staging table {target_schema_name}.{staging_table_name} after error."
                    )
        except Exception as cleanup_e:
            context.log.error(
                f"Failed to cleanup staging table {target_schema_name}.{staging_table_name}: {cleanup_e}"
            )
        raise


# --- Dimension Loader Assets ---
# Define a common retry policy and concurrency tag
DIM_LOADER_RETRY_POLICY = RetryPolicy(
    max_retries=2, delay=60
)  # Retry 2 times, 60s delay
DIM_LOADER_CONCURRENCY_TAGS = {
    "dagster/concurrency_key": "mssql_dimension_upsert",
    "dagster/max_concurrent_runs": "1",
}


# --- DimDate ---
@asset(
    name="dim_date_loader",
    deps=[create_dim_date_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Generates and UPSERTS data into the DimDate table.",
    retry_policy=DIM_LOADER_RETRY_POLICY,
    tags=DIM_LOADER_CONCURRENCY_TAGS,
)
def dim_date_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_orders_df: pd.DataFrame,
    raw_order_items_df: pd.DataFrame,
    raw_marketing_qualified_leads_df: pd.DataFrame,
    raw_closed_deals_df: pd.DataFrame,
) -> Output[dict]:
    # ... (rest of DimDate logic remains the same, ending with call to _upsert_to_db_via_staging)
    all_dates = set()

    def extract_dates_from_column(df, column_name):
        if column_name in df.columns:
            dates = (
                pd.to_datetime(df[column_name], errors="coerce").dropna().dt.normalize()
            )
            for d in dates:
                all_dates.add(d)
        else:
            context.log.warning(f"Column '{column_name}' not found for DimDate.")

    order_date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in order_date_cols:
        extract_dates_from_column(raw_orders_df, col)
    extract_dates_from_column(raw_order_items_df, "shipping_limit_date")
    extract_dates_from_column(raw_marketing_qualified_leads_df, "first_contact_date")
    extract_dates_from_column(raw_closed_deals_df, "won_date")

    target_dim_date_columns = [
        "date_key",
        "full_date",
        "day",
        "month",
        "year",
        "quarter",
        "day_of_week",
        "day_name",
        "month_name",
        "is_weekend",
        "is_holiday",
    ]
    if not all_dates:
        context.log.warning("No dates found for DimDate. Skipping UPSERT.")
        return Output(
            value={
                "table": "olist.DIM_DATE",
                "rows_inserted": 0,
                "rows_updated": 0,
                "status": "No dates found",
                "operation": "upsert_skipped_empty_df",
            },
            metadata={
                "num_rows_processed_in_df": 0,
                "columns": target_dim_date_columns,
                "destination_table": "olist.DIM_DATE",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
            },
        )

    unique_dates_df = pd.DataFrame({"full_date": sorted(list(all_dates))})
    final_df = pd.DataFrame(columns=target_dim_date_columns)
    final_df["full_date"] = unique_dates_df["full_date"]
    final_df["date_key"] = final_df["full_date"].dt.strftime("%Y%m%d").astype(int)
    final_df["day"] = final_df["full_date"].dt.day
    final_df["month"] = final_df["full_date"].dt.month
    final_df["year"] = final_df["full_date"].dt.year
    final_df["quarter"] = final_df["full_date"].dt.quarter
    final_df["day_of_week"] = final_df["full_date"].dt.dayofweek + 1
    final_df["day_name"] = final_df["full_date"].dt.strftime("%A")
    final_df["month_name"] = final_df["full_date"].dt.strftime("%B")
    final_df["is_weekend"] = final_df["day_of_week"].isin([6, 7])
    final_df["is_holiday"] = False

    return _upsert_to_db_via_staging(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_DATE",
        "olist",
        ["date_key"],
        target_dim_date_columns,
    )


@asset(
    name="dim_product_loader",
    deps=[create_dim_product_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms and UPSERTS data into the DimProduct table.",
    retry_policy=DIM_LOADER_RETRY_POLICY,
    tags=DIM_LOADER_CONCURRENCY_TAGS,
)
def dim_product_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_products_df: pd.DataFrame,
    raw_product_category_name_translation_df: pd.DataFrame,
) -> Output[dict]:
    # ... (rest of DimProduct logic remains the same)
    dim_df_merged = pd.merge(
        raw_products_df,
        raw_product_category_name_translation_df,
        on="product_category_name",
        how="left",
    )
    target_cols_for_df = [
        "product_id",
        "product_category_name",
        "product_category_name_english",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
        "product_photos_qty",
    ]
    final_df = _prepare_df_for_load(
        context, dim_df_merged, target_cols_for_df, "product_id"
    )
    return _upsert_to_db_via_staging(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_PRODUCT",
        "olist",
        ["product_id"],
        target_cols_for_df,
    )


@asset(
    name="dim_customer_loader",
    deps=[create_dim_customer_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms and UPSERTS data into the DimCustomer table.",
    retry_policy=DIM_LOADER_RETRY_POLICY,
    tags=DIM_LOADER_CONCURRENCY_TAGS,
)
def dim_customer_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_customers_df: pd.DataFrame,
    raw_geolocation_df: pd.DataFrame,
) -> Output[dict]:
    # ... (rest of DimCustomer logic remains the same)
    raw_geolocation_df["geolocation_zip_code_prefix"] = raw_geolocation_df[
        "geolocation_zip_code_prefix"
    ].astype(int)
    raw_customers_df["customer_zip_code_prefix"] = raw_customers_df[
        "customer_zip_code_prefix"
    ].astype(int)
    avg_geo_df = (
        raw_geolocation_df.groupby("geolocation_zip_code_prefix")
        .agg(
            customer_geolocation_lat=("geolocation_lat", "mean"),
            customer_geolocation_lng=("geolocation_lng", "mean"),
        )
        .reset_index()
    )
    dim_df_merged = pd.merge(
        raw_customers_df,
        avg_geo_df,
        left_on="customer_zip_code_prefix",
        right_on="geolocation_zip_code_prefix",
        how="left",
    )
    target_cols_for_df = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
        "customer_geolocation_lat",
        "customer_geolocation_lng",
    ]
    final_df = _prepare_df_for_load(
        context, dim_df_merged, target_cols_for_df, "customer_id"
    )
    return _upsert_to_db_via_staging(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_CUSTOMER",
        "olist",
        ["customer_id"],
        target_cols_for_df,
    )


@asset(
    name="dim_seller_loader",
    deps=[create_dim_seller_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms and UPSERTS data into the DimSeller table.",
    retry_policy=DIM_LOADER_RETRY_POLICY,
    tags=DIM_LOADER_CONCURRENCY_TAGS,
)
def dim_seller_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_sellers_df: pd.DataFrame,
    raw_closed_deals_df: pd.DataFrame,
) -> Output[dict]:
    # ... (rest of DimSeller logic remains the same)
    closed_deals_info = raw_closed_deals_df.sort_values("won_date").drop_duplicates(
        "seller_id", keep="first"
    )
    dim_df_merged = pd.merge(
        raw_sellers_df,
        closed_deals_info[
            [
                "seller_id",
                "business_segment",
                "lead_type",
                "lead_behaviour_profile",
                "won_date",
            ]
        ],
        on="seller_id",
        how="left",
    )
    dim_df_merged = dim_df_merged.rename(
        columns={
            "won_date": "closed_deal_date",
            "lead_behaviour_profile": "lead_behavior_profile",
        }
    )
    dim_df_merged["has_company"] = pd.NA
    dim_df_merged["has_gtin"] = pd.NA
    target_cols_for_df = [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
        "business_segment",
        "lead_type",
        "lead_behavior_profile",
        "has_company",
        "has_gtin",
        "closed_deal_date",
    ]
    final_df = _prepare_df_for_load(
        context, dim_df_merged, target_cols_for_df, "seller_id"
    )
    return _upsert_to_db_via_staging(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_SELLER",
        "olist",
        ["seller_id"],
        target_cols_for_df,
    )


@asset(
    name="dim_order_loader",
    deps=[create_dim_order_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms and UPSERTS data into the DimOrder table.",
    retry_policy=DIM_LOADER_RETRY_POLICY,
    tags=DIM_LOADER_CONCURRENCY_TAGS,
)
def dim_order_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_orders_df: pd.DataFrame,
    raw_order_payments_df: pd.DataFrame,
) -> Output[dict]:
    # ... (rest of DimOrder logic remains the same)
    payments_agg = (
        raw_order_payments_df.groupby("order_id")
        .agg(
            payment_type=("payment_type", "first"),
            payment_installments=("payment_installments", "max"),
            payment_value=("payment_value", "sum"),
        )
        .reset_index()
    )
    dim_df_merged = pd.merge(raw_orders_df, payments_agg, on="order_id", how="left")
    target_cols_for_df = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "payment_type",
        "payment_installments",
        "payment_value",
    ]
    for col in [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        if col in dim_df_merged.columns:
            dim_df_merged[col] = pd.to_datetime(dim_df_merged[col], errors="coerce")
    final_df = _prepare_df_for_load(
        context, dim_df_merged, target_cols_for_df, "order_id"
    )
    return _upsert_to_db_via_staging(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_ORDER",
        "olist",
        ["order_id"],
        target_cols_for_df,
    )


@asset(
    name="dim_marketing_loader",
    deps=[create_dim_marketing_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms and UPSERTS data into the DimMarketing table.",
    retry_policy=DIM_LOADER_RETRY_POLICY,
    tags=DIM_LOADER_CONCURRENCY_TAGS,
)
def dim_marketing_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_marketing_qualified_leads_df: pd.DataFrame,
    raw_closed_deals_df: pd.DataFrame,
) -> Output[dict]:
    # ... (rest of DimMarketing logic remains the same)
    dim_df_merged = pd.merge(
        raw_marketing_qualified_leads_df,
        raw_closed_deals_df[["mql_id", "sdr_id", "sr_id", "won_date"]],
        on="mql_id",
        how="left",
    )
    dim_df_merged["first_contact_date"] = pd.to_datetime(
        dim_df_merged["first_contact_date"], errors="coerce"
    )
    dim_df_merged["won_date"] = pd.to_datetime(
        dim_df_merged["won_date"], errors="coerce"
    )
    dim_df_merged["lead_conversion_time"] = (
        dim_df_merged["won_date"] - dim_df_merged["first_contact_date"]
    ).dt.days
    dim_df_merged["lead_conversion_time"] = dim_df_merged[
        "lead_conversion_time"
    ].astype("Float64")
    dim_df_merged = dim_df_merged.rename(columns={"origin": "traffic_source"})
    target_cols_for_df = [
        "mql_id",
        "first_contact_date",
        "landing_page_id",
        "traffic_source",
        "lead_conversion_time",
        "sdr_id",
        "sr_id",
    ]
    final_df = _prepare_df_for_load(
        context, dim_df_merged, target_cols_for_df, "mql_id"
    )
    return _upsert_to_db_via_staging(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_MARKETING",
        "olist",
        ["mql_id"],
        target_cols_for_df,
    )
