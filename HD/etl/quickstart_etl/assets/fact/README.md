# Fact Assets Module

This module contains the refactored fact table processing logic, previously contained in a single large `fact_assets.py` file. The code has been broken down into smaller, more maintainable modules.

## Module Structure

```
fact/
├── __init__.py                 # Module exports
├── fact_order_item.py         # Main fact order item asset
├── db_operations.py           # Database operations utilities
├── dimension_lookups.py       # Dimension key lookup utilities
└── data_transformations.py    # Data transformation utilities
```

## Modules Overview

### `fact_order_item.py`

Contains the main Dagster asset `fact_order_item_load_asset` that orchestrates the ETL process for loading fact order item data. This is the entry point for the fact table processing.

**Key responsibilities:**

- Partition time window handling
- Orchestrating data flow between transformation modules
- Asset metadata and logging

### `db_operations.py`

Contains database-specific operations for fact table loading.

**Key functions:**

- `delete_partition_and_append_fact_to_db()`: Handles the delete-and-insert pattern for partition loading

**Key responsibilities:**

- SQL operations for partition deletion
- Bulk data loading to SQL Server
- Transaction management
- Metadata tracking for MaterializeResult

### `dimension_lookups.py`

Contains utilities for fetching and merging dimension keys from dimension tables.

**Key functions:**

- `fetch_dimension_keys()`: Main orchestrator for dimension lookups
- `_process_date_dimension()`: Date dimension specific processing
- `_process_product_dimension()`: Product dimension lookups
- `_process_seller_dimension()`: Seller dimension lookups
- `_process_order_dimension()`: Order dimension lookups
- `_process_customer_dimension()`: Customer dimension lookups

**Key responsibilities:**

- Database queries for dimension tables
- Key mapping and merging
- Date handling and timezone conversion for date dimensions

### `data_transformations.py`

Contains data transformation and preparation utilities.

**Key functions:**

- `filter_orders_by_partition()`: Filters raw order data by partition window
- `process_review_scores()`: Aggregates and merges review scores
- `prepare_final_fact_dataframe()`: Final data preparation and validation
- `create_empty_partition_result()`: Handles empty partition scenarios

**Key responsibilities:**

- Data filtering and partitioning
- Data type conversions
- Foreign key validation
- Empty data handling

## Usage

The main asset can be imported and used as follows:

```python
from quickstart_etl.assets.fact import fact_order_item_load_asset
```

Or through the main assets module:

```python
from quickstart_etl.assets import fact_order_item_load_asset
```

## Benefits of This Refactoring

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Maintainability**: Smaller files are easier to understand and modify
3. **Testability**: Individual functions can be unit tested more easily
4. **Reusability**: Utility functions can be reused across different fact assets
5. **Readability**: Clear module structure makes the codebase more navigable

## Migration Notes

- The original `fact_assets.py` has been backed up as `fact_assets.py.backup`
- All imports have been updated to use the new modular structure
- No changes to the asset behavior or external API
- The asset continues to support partitioned loading with the same configuration
