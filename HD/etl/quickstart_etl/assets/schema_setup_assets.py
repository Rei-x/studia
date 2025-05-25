from dagster import asset, AssetExecutionContext, Output
from sqlalchemy import text

from quickstart_etl.resources.db_resource import SQLAlchemyResource


SCHEMA_NAME = "olist"


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
    payment_type NVARCHAR(30) NULL,
    payment_installments INT NULL,
    payment_value DECIMAL(10, 2) NULL
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

    price DECIMAL(10, 2) NOT NULL,
    freight_value DECIMAL(10, 2) NOT NULL,
    total_value AS (price + freight_value) PERSISTED,

    -- From your DDL: Miary nieaddytywne
    -- delivery_days FLOAT NULL, -- This is better calculated in ETL or derived via DimOrder
    review_score FLOAT NULL -- This is better calculated in ETL or derived via DimOrder/DimReview
)
"""


CREATE_FACT_ORDER_ITEM_DDL_DOC = f"""
CREATE TABLE {SCHEMA_NAME}.FACT_ORDER_ITEM (
    order_item_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_key INT NOT NULL,
    product_key INT NOT NULL,
    seller_key INT NOT NULL,
    customer_key INT NOT NULL,
    date_key INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    freight_value DECIMAL(10, 2) NOT NULL,
    total_value AS (price + freight_value) PERSISTED,
    delivery_days FLOAT NULL,
    review_score FLOAT NULL
)
"""


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


DROP_FACT_ORDER_ITEM_DDL = f"DROP TABLE IF EXISTS {SCHEMA_NAME}.FACT_ORDER_ITEM"
DROP_DIM_ORDER_DDL = f"DROP TABLE IF EXISTS {SCHEMA_NAME}.DIM_ORDER"
DROP_DIM_SELLER_DDL = f"DROP TABLE IF EXISTS {SCHEMA_NAME}.DIM_SELLER"
DROP_DIM_CUSTOMER_DDL = f"DROP TABLE IF EXISTS {SCHEMA_NAME}.DIM_CUSTOMER"
DROP_DIM_PRODUCT_DDL = f"DROP TABLE IF EXISTS {SCHEMA_NAME}.DIM_PRODUCT"
DROP_DIM_DATE_DDL = f"DROP TABLE IF EXISTS {SCHEMA_NAME}.DIM_DATE"


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
            connection.commit()
        context.log.info(f"Successfully executed DDL: {statement_name}")
        return Output(value={"status": "Success", "ddl_statement": statement_name})
    except Exception as e:
        error_message = str(e).lower()
        if (
            "already an object named" in error_message
            or "already exists" in error_message
            or "already has a primary key" in error_message
            or "does not exist"
            in error_message  # Handle DROP TABLE IF EXISTS for non-existent tables
            or "could not drop" in error_message
            and "does not exist" in error_message
            or "constraint" in error_message
            and (
                "already exists" in error_message or "could not create" in error_message
            )
        ):
            context.log.warning(
                f"DDL for '{statement_name}' likely already applied or object doesn't exist: {e}"
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


@asset(
    name="olist_schema",
    group_name="schema_setup",
    compute_kind="sql_ddl",
    description=f"Creates the '{SCHEMA_NAME}' schema if it doesn't exist.",
)
def olist_schema(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    tables_to_drop = {
        "FACT_ORDER_ITEM": DROP_FACT_ORDER_ITEM_DDL,
        "DIM_ORDER": DROP_DIM_ORDER_DDL,
        "DIM_SELLER": DROP_DIM_SELLER_DDL,
        "DIM_CUSTOMER": DROP_DIM_CUSTOMER_DDL,
        "DIM_PRODUCT": DROP_DIM_PRODUCT_DDL,
        "DIM_DATE": DROP_DIM_DATE_DDL,
    }

    results = []
    all_successful = True

    for table_name, ddl in tables_to_drop.items():
        try:
            output = _execute_ddl(
                context, sql_alchemy_resource, ddl, f"Drop {table_name} Table"
            )
            results.append(output.value)
            if (
                output.value.get("status") != "Success"
                and output.value.get("status") != "Already Exists or No-op"
            ):
                all_successful = False
        except Exception as e:
            context.log.error(f"Failed to drop table {table_name}: {e}")
            results.append({"status": "Failed", "table": table_name, "error": str(e)})
            all_successful = False

    final_status = "Success" if all_successful else "Partial Success or Failure"
    context.log.info(f"Schema cleanup status: {final_status}")

    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_SCHEMA_DDL, f"Create Schema {SCHEMA_NAME}"
    )


@asset(
    name="dim_date_table",
    group_name="schema_setup",
    deps=[olist_schema],
    compute_kind="sql_ddl",
)
def dim_date_table(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_DIM_DATE_DDL, "Create DIM_DATE Table"
    )


@asset(
    name="dim_product_table",
    group_name="schema_setup",
    deps=[olist_schema],
    compute_kind="sql_ddl",
)
def dim_product_table(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_DIM_PRODUCT_DDL,
        "Create DIM_PRODUCT Table",
    )


@asset(
    name="dim_customer_table",
    group_name="schema_setup",
    deps=[olist_schema],
    compute_kind="sql_ddl",
)
def dim_customer_table(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_DIM_CUSTOMER_DDL,
        "Create DIM_CUSTOMER Table",
    )


@asset(
    name="dim_seller_table",
    group_name="schema_setup",
    deps=[olist_schema],
    compute_kind="sql_ddl",
)
def dim_seller_table(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_DIM_SELLER_DDL, "Create DIM_SELLER Table"
    )


@asset(
    name="dim_order_table",
    group_name="schema_setup",
    deps=[olist_schema],
    compute_kind="sql_ddl",
)
def dim_order_table(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context, sql_alchemy_resource, CREATE_DIM_ORDER_DDL, "Create DIM_ORDER Table"
    )


@asset(
    name="fact_order_item_table",
    group_name="schema_setup",
    deps=[olist_schema],
    compute_kind="sql_ddl",
)
def fact_order_item_table(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    return _execute_ddl(
        context,
        sql_alchemy_resource,
        CREATE_FACT_ORDER_ITEM_DDL_DOC,
        "Create FACT_ORDER_ITEM Table",
    )


@asset(
    name="foreign_key_constraints",
    group_name="schema_setup",
    deps=[
        dim_date_table,
        dim_product_table,
        dim_customer_table,
        dim_seller_table,
        dim_order_table,
        fact_order_item_table,
    ],
    compute_kind="sql_ddl",
    description="Applies foreign key constraints to FACT_ORDER_ITEM.",
)
def foreign_key_constraints(
    context: AssetExecutionContext, sql_alchemy_resource: SQLAlchemyResource
) -> Output[dict]:
    fks_to_apply = {
        "FK_OrderItem_Date": FK_ORDERITEM_DATE_DDL,
        "FK_OrderItem_Product": FK_ORDERITEM_PRODUCT_DDL,
        "FK_OrderItem_Customer": FK_ORDERITEM_CUSTOMER_DDL,
        "FK_OrderItem_Seller": FK_ORDERITEM_SELLER_DDL,
        "FK_OrderItem_Order": FK_ORDERITEM_ORDER_DDL,
    }
    results = []
    all_successful = True
    for fk_name, ddl in fks_to_apply.items():
        output = _execute_ddl(context, sql_alchemy_resource, ddl, f"Apply FK {fk_name}")
        results.append(output.value)
        if (
            output.value.get("status") != "Success"
            and output.value.get("status") != "Already Exists or No-op"
        ):
            all_successful = False

    final_status = "Success" if all_successful else "Partial Success or Failure"
    context.log.info(f"Foreign key application status: {final_status}")
    return Output(value={"status": final_status, "fk_results": results})
