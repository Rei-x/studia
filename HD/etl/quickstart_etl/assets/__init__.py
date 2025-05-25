# filepath: /home/rei/projects/studia/HD/etl/quickstart_etl/assets/__init__.py
from quickstart_etl.assets.dims import (
    dim_date_load_asset,
    dim_product_load_asset,
    dim_customer_load_asset,
    dim_seller_load_asset,
    dim_order_load_asset,
)

# Import specific assets from other modules
from quickstart_etl.assets.schema_setup_assets import (
    create_dim_date_table_asset,
    create_dim_product_table_asset,
    create_dim_customer_table_asset,
    create_dim_seller_table_asset,
    create_dim_order_table_asset,
    create_fact_order_item_table_asset,
    create_olist_schema_asset,
    apply_foreign_keys_asset,
)

from quickstart_etl.assets.raw_data import (
    raw_orders_df,
    raw_order_items_df,
    raw_order_payments_df,
    raw_order_reviews_df,
    raw_customers_df,
    raw_products_df,
    raw_product_category_name_translation_df,
    raw_sellers_df,
    raw_geolocation_df,
    raw_closed_deals_df,
    raw_marketing_qualified_leads_df,
)

from quickstart_etl.assets.fact import (
    fact_order_item_load_asset,
)

# Export all assets
__all__ = [
    # Dimension assets
    "dim_date_load_asset",
    "dim_product_load_asset",
    "dim_customer_load_asset",
    "dim_seller_load_asset",
    "dim_order_load_asset",
    # Schema setup assets
    "create_dim_date_table_asset",
    "create_dim_product_table_asset",
    "create_dim_customer_table_asset",
    "create_dim_seller_table_asset",
    "create_dim_order_table_asset",
    "create_fact_order_item_table_asset",
    "create_olist_schema_asset",
    "apply_foreign_keys_asset",
    # Raw data assets
    "raw_orders_df",
    "raw_order_items_df",
    "raw_order_payments_df",
    "raw_order_reviews_df",
    "raw_customers_df",
    "raw_products_df",
    "raw_product_category_name_translation_df",
    "raw_sellers_df",
    "raw_geolocation_df",
    "raw_closed_deals_df",
    "raw_marketing_qualified_leads_df",
    # Fact assets
    "fact_order_item_load_asset",
]
