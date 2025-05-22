# olist_etl/assets/dimension_assets.py

import pandas as pd
from dagster import asset, Output, AssetExecutionContext
from sqlalchemy import text, Engine  # For executing TRUNCATE

# Assuming your SQLAlchemyResource is correctly imported
from quickstart_etl.resources.db_resource import SQLAlchemyResource  # Using your path

# Import the DDL assets that create the tables
from .schema_setup_assets import (  # Adjust path if your schema assets are elsewhere
    create_dim_date_table_asset,
    create_dim_product_table_asset,
    create_dim_customer_table_asset,
    create_dim_seller_table_asset,
    create_dim_order_table_asset,
    create_dim_marketing_table_asset,
)


def _prepare_df_for_load(
    context: AssetExecutionContext,
    df_merged: pd.DataFrame,
    target_columns: list[str],
    business_key_column: str | None = None,
) -> pd.DataFrame:
    """
    Ensures the DataFrame has all target columns, fills missing ones with NA,
    and optionally drops rows where the business key is NA.
    """
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


def _truncate_and_append_to_db(
    context: AssetExecutionContext,
    engine: Engine,  # Changed from SQLAlchemyResource to Engine for more direct use
    final_df: pd.DataFrame,
    table_name: str,
    schema_name: str,
    target_columns_for_metadata: list[str],  # For consistent metadata when df is empty
) -> Output[dict]:
    """
    Truncates the specified table and appends the DataFrame.
    Returns a Dagster Output object with load metadata.
    """
    rows_loaded = 0
    try:
        with engine.connect() as connection:
            truncate_statement = text(f"DELETE FROM {schema_name}.{table_name}")
            connection.execute(truncate_statement)
            connection.commit()
            context.log.info(
                f"Successfully truncated table {schema_name}.{table_name}."
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
                f"Successfully appended {len(final_df)} rows into {schema_name}.{table_name}."
            )
            rows_loaded = len(final_df)
        else:
            context.log.info(f"No data to append to {schema_name}.{table_name}.")

        return Output(
            value={
                "table": f"{schema_name}.{table_name}",
                "rows_loaded": rows_loaded,
                "operation": "truncate_append",
            },
            metadata={
                "num_rows": rows_loaded,
                "columns": list(final_df.columns)
                if not final_df.empty
                else target_columns_for_metadata,
                "destination_table": f"{schema_name}.{table_name}",
                "source": "olist_dwh",  # Consistent metadata key
                "load_time": pd.Timestamp.now().isoformat(),
            },
        )
    except Exception as e:
        context.log.error(
            f"Failed to truncate/load data to {schema_name}.{table_name}: {e}"
        )
        raise


# --- Dimension Loader Assets ---


# --- DimDate ---
@asset(
    name="dim_date_loader",
    deps=[create_dim_date_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Generates, truncates, and loads the DimDate table to SQL Server.",
)
def dim_date_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_orders_df: pd.DataFrame,
    raw_order_items_df: pd.DataFrame,
    raw_marketing_qualified_leads_df: pd.DataFrame,
    raw_closed_deals_df: pd.DataFrame,
) -> Output[dict]:
    all_dates = set()

    def extract_dates_from_column(df, column_name):
        if column_name in df.columns:
            dates = (
                pd.to_datetime(df[column_name], errors="coerce").dropna().dt.normalize()
            )
            for d in dates:
                all_dates.add(d)
        else:
            context.log.warning(
                f"Column '{column_name}' not found for DimDate generation."
            )

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

    if not all_dates:
        context.log.warning("No dates found for DimDate.")
        # Return an Output consistent with _truncate_and_append_to_db for an empty load
        return Output(
            value={
                "table": "olist.DIM_DATE",
                "rows_loaded": 0,
                "status": "No dates found",
                "operation": "truncate_append",
            },
            metadata={
                "num_rows": 0,
                "columns": [  # Define expected columns for consistency
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
                ],
                "destination_table": "olist.DIM_DATE",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
                "status_detail": "No dates found in source",
            },
        )

    unique_dates_df = pd.DataFrame({"full_date": sorted(list(all_dates))})
    dim_df = pd.DataFrame()
    dim_df["full_date"] = unique_dates_df["full_date"]
    dim_df["date_key"] = dim_df["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_df["day"] = dim_df["full_date"].dt.day
    dim_df["month"] = dim_df["full_date"].dt.month
    dim_df["year"] = dim_df["full_date"].dt.year
    dim_df["quarter"] = dim_df["full_date"].dt.quarter
    dim_df["day_of_week"] = dim_df["full_date"].dt.dayofweek + 1
    dim_df["day_name"] = dim_df["full_date"].dt.strftime("%A")
    dim_df["month_name"] = dim_df["full_date"].dt.strftime("%B")
    dim_df["is_weekend"] = dim_df["day_of_week"].isin([6, 7])
    dim_df["is_holiday"] = False
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
    final_df = dim_df[target_dim_date_columns].copy()

    return _truncate_and_append_to_db(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_DATE",
        "olist",
        target_dim_date_columns,
    )


# --- DimProduct ---
@asset(
    name="dim_product_loader",
    deps=[create_dim_product_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms, truncates, and loads the DimProduct table.",
)
def dim_product_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_products_df: pd.DataFrame,
    raw_product_category_name_translation_df: pd.DataFrame,
) -> Output[dict]:
    dim_df_merged = pd.merge(
        raw_products_df,
        raw_product_category_name_translation_df,
        on="product_category_name",
        how="left",
    )
    target_columns = [
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
        context, dim_df_merged, target_columns, "product_id"
    )
    return _truncate_and_append_to_db(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_PRODUCT",
        "olist",
        target_columns,
    )


# --- DimCustomer ---
@asset(
    name="dim_customer_loader",
    deps=[create_dim_customer_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms, truncates, and loads the DimCustomer table.",
)
def dim_customer_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_customers_df: pd.DataFrame,
    raw_geolocation_df: pd.DataFrame,
) -> Output[dict]:
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
    target_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
        "customer_geolocation_lat",
        "customer_geolocation_lng",
    ]
    final_df = _prepare_df_for_load(
        context, dim_df_merged, target_columns, "customer_id"
    )
    return _truncate_and_append_to_db(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_CUSTOMER",
        "olist",
        target_columns,
    )


# --- DimSeller ---
@asset(
    name="dim_seller_loader",
    deps=[create_dim_seller_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms, truncates, and loads the DimSeller table.",
)
def dim_seller_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_sellers_df: pd.DataFrame,
    raw_closed_deals_df: pd.DataFrame,
) -> Output[dict]:
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
    dim_df_merged["has_company"] = (
        pd.NA
    )  # Assuming these columns are not in source, add as NA
    dim_df_merged["has_gtin"] = pd.NA
    target_columns = [
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
    final_df = _prepare_df_for_load(context, dim_df_merged, target_columns, "seller_id")
    return _truncate_and_append_to_db(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_SELLER",
        "olist",
        target_columns,
    )


# --- DimOrder ---
@asset(
    name="dim_order_loader",
    deps=[create_dim_order_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms, truncates, and loads the DimOrder table.",
)
def dim_order_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_orders_df: pd.DataFrame,
    raw_order_payments_df: pd.DataFrame,
) -> Output[dict]:
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

    target_columns = [
        "order_id",
        "order_status",
        "payment_type",
        "payment_installments",
        "payment_value",
    ]
    final_df = _prepare_df_for_load(context, dim_df_merged, target_columns, "order_id")
    return _truncate_and_append_to_db(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_ORDER",
        "olist",
        target_columns,
    )


@asset(
    name="dim_marketing_loader",
    deps=[create_dim_marketing_table_asset],
    group_name="dimensions_loaders",
    key_prefix=["olist_dwh"],
    compute_kind="sqlalchemy",
    description="Transforms, truncates, and loads the DimMarketing table.",
)
def dim_marketing_load_asset(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    raw_marketing_qualified_leads_df: pd.DataFrame,
    raw_closed_deals_df: pd.DataFrame,
) -> Output[dict]:
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
    target_columns = [
        "mql_id",
        "first_contact_date",
        "landing_page_id",
        "traffic_source",
        "lead_conversion_time",
        "sdr_id",
        "sr_id",
    ]
    final_df = _prepare_df_for_load(context, dim_df_merged, target_columns, "mql_id")
    return _truncate_and_append_to_db(
        context,
        sql_alchemy_resource.get_engine(),
        final_df,
        "DIM_MARKETING",
        "olist",
        target_columns,
    )
