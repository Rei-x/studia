# olist_etl/assets/schema_setup_assets.py

from dagster import asset, AssetExecutionContext, Output
from sqlalchemy import text

from quickstart_etl.resources.db_resource import SQLAlchemyResource


SCHEMA_NAME = "olist"

# --- DDL Statements (extracted from your document) ---

CREATE_SCHEMA_DDL = f"IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{SCHEMA_NAME}') EXEC('CREATE SCHEMA {SCHEMA_NAME}')"

CREATE_DIM_DATE_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.DIM_DATE (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name NVARCHAR(20) NOT NULL,
    month_name NVARCHAR(20) NOT NULL,
    is_weekend BIT NOT NULL,
    is_holiday BIT NOT NULL
)
"""

CREATE_DIM_PRODUCT_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.DIM_PRODUCT (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id NVARCHAR(50) NOT NULL,
    product_category_name NVARCHAR(100) NULL,
    product_category_name_english NVARCHAR(100) NULL,
    product_weight_g FLOAT NULL,
    product_length_cm FLOAT NULL,
    product_height_cm FLOAT NULL,
    product_width_cm FLOAT NULL,
    product_volume_cm3 AS (product_length_cm * product_height_cm * product_width_cm) PERSISTED,
    product_photos_qty INT NULL
)
"""

CREATE_DIM_CUSTOMER_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.DIM_CUSTOMER (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id NVARCHAR(50) NOT NULL,
    customer_unique_id NVARCHAR(50) NOT NULL,
    customer_zip_code_prefix NVARCHAR(20) NULL,
    customer_city NVARCHAR(100) NULL,
    customer_state NVARCHAR(2) NULL,
    customer_geolocation_lat FLOAT NULL,
    customer_geolocation_lng FLOAT NULL
)
"""

CREATE_DIM_SELLER_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.DIM_SELLER (
    seller_key INT IDENTITY(1,1) PRIMARY KEY,
    seller_id NVARCHAR(50) NOT NULL,
    seller_zip_code_prefix NVARCHAR(20) NULL,
    seller_city NVARCHAR(100) NULL,
    seller_state NVARCHAR(2) NULL,
    business_segment NVARCHAR(50) NULL,
    lead_type NVARCHAR(50) NULL,
    lead_behavior_profile NVARCHAR(50) NULL,
    has_company BIT NULL,
    has_gtin BIT NULL,
    closed_deal_date DATETIME NULL
)
"""

CREATE_DIM_ORDER_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.DIM_ORDER (
    order_key INT IDENTITY(1,1) PRIMARY KEY,
    order_id NVARCHAR(50) NOT NULL,
    order_status NVARCHAR(30) NULL,
    order_purchase_timestamp DATETIME NULL,
    order_approved_at DATETIME NULL,
    order_delivered_carrier_date DATETIME NULL,
    order_delivered_customer_date DATETIME NULL,
    order_estimated_delivery_date DATETIME NULL,
    delivery_delay_days AS
        CASE
            WHEN order_delivered_customer_date IS NOT NULL AND order_estimated_delivery_date IS NOT NULL
            THEN DATEDIFF(DAY, order_estimated_delivery_date, order_delivered_customer_date)
            ELSE NULL
        END PERSISTED,
    payment_type NVARCHAR(30) NULL,
    payment_installments INT NULL,
    payment_value DECIMAL(10, 2) NULL
)
"""

CREATE_DIM_MARKETING_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.DIM_MARKETING (
    marketing_key INT IDENTITY(1,1) PRIMARY KEY,
    mql_id NVARCHAR(50) NULL,
    first_contact_date DATE NULL,
    landing_page_id NVARCHAR(50) NULL,
    traffic_source NVARCHAR(50) NULL,
    lead_conversion_time INT NULL,
    sdr_id NVARCHAR(50) NULL,
    sr_id NVARCHAR(50) NULL
)
"""

CREATE_FACT_ORDER_ITEM_DDL = f"""
CREATE TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM (
    order_item_id BIGINT IDENTITY(1,1) PRIMARY KEY, -- Changed from your document's example, as order_item_id from source is not unique across orders
    order_id NVARCHAR(50) NOT NULL, -- Added to link to orders easily and for FK to DimOrder if order_item_id from source is used as FK
    source_order_item_id INT NOT NULL, -- Original order_item_id from source data, might be 1,2,3 per order
    product_id NVARCHAR(50) NOT NULL, -- Added for easier FK to DimProduct
    seller_id NVARCHAR(50) NOT NULL, -- Added for easier FK to DimSeller
    customer_id NVARCHAR(50) NULL, -- Added for FK to DimCustomer (via order)
    shipping_limit_date DATETIME NULL, -- Added for DimDate link based on shipping
    mql_id NVARCHAR(50) NULL, -- Added for potential FK to DimMarketing

    order_key INT NOT NULL,
    product_key INT NOT NULL,
    seller_key INT NOT NULL,
    customer_key INT NOT NULL,
    date_key INT NOT NULL, -- Refers to a specific date (e.g. order purchase date)
    marketing_key INT NULL,

    price DECIMAL(10, 2) NOT NULL,
    freight_value DECIMAL(10, 2) NOT NULL,
    total_value AS (price + freight_value) PERSISTED,

    -- From your DDL: Miary nieaddytywne
    -- delivery_days FLOAT NULL, -- This is better calculated in ETL or derived via DimOrder
    review_score FLOAT NULL -- This is better calculated in ETL or derived via DimOrder/DimReview
)
"""
# Note on FACT_ORDER_ITEM DDL:
# Your original DDL for FACT_ORDER_ITEM has `order_item_id BIGINT IDENTITY(1,1) PRIMARY KEY`.
# The source `olist_order_items_dataset.csv` has `order_id` and `order_item_id` (which is 1,2,3... per order).
# For clarity, I've added `source_order_item_id` for the latter and kept `order_item_id` as the surrogate PK.
# I also added business key columns (like `order_id`, `product_id`, `seller_id`) to the fact DDL stub above
# as these are crucial for joining during the ETL to look up surrogate keys. The final FKs will point to surrogate keys.
# The `date_key` in the fact table will relate to a specific event date (e.g., order purchase date, shipping date).
# Your provided FK constraints use surrogate keys, so the DDL for FACT_ORDER_ITEM needs these `_key` columns.

# The DDL for FACT_ORDER_ITEM from your document (page 24) which I will use:
CREATE_FACT_ORDER_ITEM_DDL_DOC = f"""
CREATE TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM (
    order_item_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_key INT NOT NULL,
    product_key INT NOT NULL,
    seller_key INT NOT NULL,
    customer_key INT NOT NULL,
    date_key INT NOT NULL,
    marketing_key INT NULL,
    price DECIMAL(10, 2) NOT NULL,
    freight_value DECIMAL(10, 2) NOT NULL,
    total_value AS (price + freight_value) PERSISTED,
    delivery_days FLOAT NULL,
    review_score FLOAT NULL
)
"""


# --- Foreign Key DDLs ---
FK_ORDERITEM_DATE_DDL = f"""
ALTER TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM ADD CONSTRAINT FK_OrderItem_Date
FOREIGN KEY (date_key) REFERENCES {SCHEMA_NAME}.DIM_DATE (date_key)
"""
FK_ORDERITEM_PRODUCT_DDL = f"""
ALTER TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM ADD CONSTRAINT FK_OrderItem_Product
FOREIGN KEY (product_key) REFERENCES {SCHEMA_NAME}.DIM_PRODUCT (product_key)
"""
FK_ORDERITEM_CUSTOMER_DDL = f"""
ALTER TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM ADD CONSTRAINT FK_OrderItem_Customer
FOREIGN KEY (customer_key) REFERENCES {SCHEMA_NAME}.DIM_CUSTOMER (customer_key)
"""
FK_ORDERITEM_SELLER_DDL = f"""
ALTER TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM ADD CONSTRAINT FK_OrderItem_Seller
FOREIGN KEY (seller_key) REFERENCES {SCHEMA_NAME}.DIM_SELLER (seller_key)
"""
FK_ORDERITEM_ORDER_DDL = f"""
ALTER TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM ADD CONSTRAINT FK_OrderItem_Order
FOREIGN KEY (order_key) REFERENCES {SCHEMA_NAME}.DIM_ORDER (order_key)
"""
FK_ORDERITEM_MARKETING_DDL = f"""
ALTER TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM ADD CONSTRAINT FK_OrderItem_Marketing
FOREIGN KEY (marketing_key) REFERENCES {SCHEMA_NAME}.DIM_MARKETING (marketing_key)
"""


# --- Helper function to execute DDL ---
def _execute_ddl(
    context: AssetExecutionContext,
    sql_alchemy_resource: SQLAlchemyResource,
    ddl_statement: str,
    statement_name: str,
):
    engine = sql_alchemy_resource.get_engine()
    try:
        with engine.connect() as connection:
            connection.execute(text(ddl_statement))
            connection.commit()  # For some DDL, explicit commit might be needed or auto-committed
        context.log.info(f"Successfully executed DDL: {statement_name}")
        return Output(value={"status": "Success", "ddl_statement": statement_name})
    except Exception as e:
        # Check if error is because object already exists (common for CREATE statements)
        # This depends on the specific error message from SQL Server.
        # Example: SQL Server error code 2714 for "There is already an object named '...' in the database."
        # Example: SQL Server error code 15005 for "The schema '...' already exists." (for CREATE SCHEMA)
        # Example: SQL Server error code 1779 for "Table '...' already has a primary key defined on it."
        # Example: SQL Server error code 1750 for "Could not create constraint. See previous errors."
        # Example: SQL Server error code 547 for FK violation or 1785 for FK referencing non-existent PK

        # For simplicity, we log the error. For more robust idempotency,
        # you'd parse the error or use `IF NOT EXISTS` in DDLs.
        # The CREATE_SCHEMA_DDL above already includes an IF NOT EXISTS check.
        # For tables, SQL Server 2016+ supports `CREATE TABLE IF NOT EXISTS`.
        # For older versions, you'd query sys.tables.

        error_message = str(e).lower()
        if (
            "already an object named" in error_message
            or "already exists" in error_message
            or "already has a primary key" in error_message
            or "constraint" in error_message
            and (
                "already exists" in error_message or "could not create" in error_message
            )
        ):  # Be careful with generic "constraint"
            context.log.warning(
                f"DDL for '{statement_name}' likely already applied: {e}"
            )
            return Output(
                value={
                    "status": "Already Exists or No-op",
                    "ddl_statement": statement_name,
                }
            )
        else:
            context.log.error(f"Failed to execute DDL for '{statement_name}': {e}")
            raise


# --- Schema Creation Asset ---
@asset(
    name="create_olist_schema",
    group_name="schema_setup",
    compute_kind="sql_ddl",
    description=f"Creates the '{SCHEMA_NAME}' schema if it doesn't exist.",
)
def create_olist_schema_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_SCHEMA_DDL, f"Create Schema {SCHEMA_NAME}"
    )


# --- Table Creation Assets ---
# These depend on schema creation
@asset(
    name="create_dim_date_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],
    compute_kind="sql_ddl",
)
def create_dim_date_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_DIM_DATE_DDL, "Create DIM_DATE Table"
    )


@asset(
    name="create_dim_product_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],
    compute_kind="sql_ddl",
)
def create_dim_product_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_DIM_PRODUCT_DDL,
        "Create DIM_PRODUCT Table",
    )


@asset(
    name="create_dim_customer_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],
    compute_kind="sql_ddl",
)
def create_dim_customer_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_DIM_CUSTOMER_DDL,
        "Create DIM_CUSTOMER Table",
    )


@asset(
    name="create_dim_seller_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],
    compute_kind="sql_ddl",
)
def create_dim_seller_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_DIM_SELLER_DDL, "Create DIM_SELLER Table"
    )


@asset(
    name="create_dim_order_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],
    compute_kind="sql_ddl",
)
def create_dim_order_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_DIM_ORDER_DDL, "Create DIM_ORDER Table"
    )


@asset(
    name="create_dim_marketing_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],
    compute_kind="sql_ddl",
)
def create_dim_marketing_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_DIM_MARKETING_DDL,
        "Create DIM_MARKETING Table",
    )


@asset(
    name="create_fact_order_item_table",
    group_name="schema_setup",
    deps=[create_olist_schema_asset],  # Depends on schema
    compute_kind="sql_ddl",
)
def create_fact_order_item_table_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    # Using the DDL from your document
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_FACT_ORDER_ITEM_DDL_DOC,
        "Create FACT_ORDER_ITEM Table",
    )


# --- Foreign Key Application Asset ---
# This asset depends on all table creation assets.
@asset(
    name="apply_foreign_keys",
    group_name="schema_setup",
    deps=[
        create_dim_date_table_asset,
        create_dim_product_table_asset,
        create_dim_customer_table_asset,
        create_dim_seller_table_asset,
        create_dim_order_table_asset,
        create_dim_marketing_table_asset,
        create_fact_order_item_table_asset,
    ],
    compute_kind="sql_ddl",
    description="Applies foreign key constraints to FACT_ORDER_ITEM.",
)
def apply_foreign_keys_asset(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    fks_to_apply = {
        "FK_OrderItem_Date": FK_ORDERITEM_DATE_DDL,
        "FK_OrderItem_Product": FK_ORDERITEM_PRODUCT_DDL,
        "FK_OrderItem_Customer": FK_ORDERITEM_CUSTOMER_DDL,
        "FK_OrderItem_Seller": FK_ORDERITEM_SELLER_DDL,
        "FK_OrderItem_Order": FK_ORDERITEM_ORDER_DDL,
        "FK_OrderItem_Marketing": FK_ORDERITEM_MARKETING_DDL,
    }
    results = []
    all_successful = True
    for fk_name, ddl in fks_to_apply.items():
        # Need to pass context and resource to _execute_ddl
        output = _execute_ddl(context, sql_alchemy_resource, ddl, f"Apply FK {fk_name}")
        results.append(output.value)  # Assuming _execute_ddl returns Output(value=dict)
        if (
            output.value.get("status") != "Success"
            and output.value.get("status") != "Already Exists or No-op"
        ):
            all_successful = False

    final_status = "Success" if all_successful else "Partial Success or Failure"
    context.log.info(f"Foreign key application status: {final_status}")
    return Output(value={"status": final_status, "fk_results": results})
