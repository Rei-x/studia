from dagster import AssetExecutionContext, Output, asset
import pandas as pd

from quickstart_etl.assets.dims.utils import (
    DIM_LOADER_CONCURRENCY_TAGS,
    DIM_LOADER_RETRY_POLICY,
    _upsert_to_db_via_staging,
)
from quickstart_etl.resources.db_resource import SQLAlchemyResource
from quickstart_etl.assets.schema_setup_assets import dim_date_table


@asset(
    name="dim_date_loader",
    deps=[dim_date_table],
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
