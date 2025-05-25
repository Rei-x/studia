from dagster import AssetExecutionContext, Output, asset
import pandas as pd

from quickstart_etl.assets.dims.utils import (
    DIM_LOADER_CONCURRENCY_TAGS,
    DIM_LOADER_RETRY_POLICY,
    _prepare_df_for_load,
    _upsert_to_db_via_staging,
)
from quickstart_etl.resources.db_resource import SQLAlchemyResource
from quickstart_etl.assets.schema_setup_assets import dim_customer_table


@asset(
    name="dim_customer_loader",
    deps=[dim_customer_table],
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
