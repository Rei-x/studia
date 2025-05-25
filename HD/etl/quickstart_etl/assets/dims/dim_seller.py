from dagster import AssetExecutionContext, Output, asset
import pandas as pd

from quickstart_etl.assets.dims.utils import (
    DIM_LOADER_CONCURRENCY_TAGS,
    DIM_LOADER_RETRY_POLICY,
    _prepare_df_for_load,
    _upsert_to_db_via_staging,
)
from quickstart_etl.resources.db_resource import SQLAlchemyResource
from quickstart_etl.assets.schema_setup_assets import create_dim_seller_table_asset


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
