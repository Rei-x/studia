from dagster import AssetExecutionContext, Output, asset
import pandas as pd

from quickstart_etl.assets.dims.utils import (
    DIM_LOADER_CONCURRENCY_TAGS,
    DIM_LOADER_RETRY_POLICY,
    _prepare_df_for_load,
    _upsert_to_db_via_staging,
)
from quickstart_etl.resources.db_resource import SQLAlchemyResource
from quickstart_etl.assets.schema_setup_assets import dim_product_table


@asset(
    name="dim_product_loader",
    deps=[dim_product_table],
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
    dim_df_merged = pd.merge(
        raw_products_df,
        raw_product_category_name_translation_df,
        on="product_category_name",
        how="left",
    )

    dim_df_merged = dim_df_merged[
        (dim_df_merged["product_category_name"].notna())
        & (dim_df_merged["product_weight_g"].notna())
    ]

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
