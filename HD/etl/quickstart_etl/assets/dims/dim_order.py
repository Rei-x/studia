from dagster import AssetExecutionContext, Output, asset
import pandas as pd

from quickstart_etl.assets.dims.utils import (
    DIM_LOADER_CONCURRENCY_TAGS,
    DIM_LOADER_RETRY_POLICY,
    _prepare_df_for_load,
    _upsert_to_db_via_staging,
)
from quickstart_etl.resources.db_resource import SQLAlchemyResource
from quickstart_etl.assets.schema_setup_assets import dim_order_table


@asset(
    name="dim_order_loader",
    deps=[dim_order_table],
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
        "payment_type",
        "payment_installments",
        "payment_value",
    ]
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
