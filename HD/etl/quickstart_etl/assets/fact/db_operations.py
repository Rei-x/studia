"""
Database operations utilities for fact table loading.
"""

import pandas as pd
from dagster import AssetExecutionContext, MaterializeResult
from sqlalchemy import text, Engine


def delete_partition_and_append_fact_to_db(
    context: AssetExecutionContext,
    engine: Engine,
    final_df: pd.DataFrame,
    table_name: str,
    schema_name: str,
    target_columns_for_metadata: list[str],
    partition_start_date: pd.Timestamp,  # This will be UTC-aware
    partition_end_date: pd.Timestamp,  # This will be UTC-aware and exclusive
) -> MaterializeResult:
    """
    Delete existing data for a partition and append new data to the fact table.

    Args:
        context: Dagster asset execution context
        engine: SQLAlchemy engine
        final_df: DataFrame to load
        table_name: Target table name
        schema_name: Target schema name
        target_columns_for_metadata: List of expected columns for metadata
        partition_start_date: Start of partition window (inclusive)
        partition_end_date: End of partition window (exclusive)

    Returns:
        MaterializeResult with metadata about the operation
    """
    rows_loaded = 0

    # For the DELETE statement, we need to ensure DIM_DATE.full_date comparison is correct.
    # If DIM_DATE.full_date is stored as a naive date, we might need to convert
    # partition_start_date and partition_end_date to naive for the SQL query parameters,
    # or ensure DIM_DATE also stores tz-aware dates (e.g., UTC).
    # For now, let's assume DIM_DATE.full_date is a DATE type and comparison with
    # timezone-aware timestamps passed as parameters will be handled correctly by the DB driver
    # (often by converting the tz-aware timestamp to the DB's session timezone or UTC before comparison).
    # It's safer if DIM_DATE also stores UTC dates if possible.
    # We'll pass the tz-aware timestamps directly to the SQL query.
    sql_partition_start_dt = partition_start_date
    sql_partition_end_exclusive_dt = partition_end_date

    try:
        with engine.connect() as connection:
            delete_statement = text(f"""
                DELETE ft
                FROM {schema_name}.{table_name} ft
                JOIN {schema_name}.DIM_DATE dd ON ft.date_key = dd.date_key
                WHERE dd.full_date >= :partition_start AND dd.full_date < :partition_end_exclusive
            """)
            result = connection.execute(
                delete_statement,
                {
                    "partition_start": sql_partition_start_dt,
                    "partition_end_exclusive": sql_partition_end_exclusive_dt,
                },
            )
            connection.commit()
            context.log.info(
                f"Deleted {result.rowcount} existing rows for partition {partition_start_date.strftime('%Y-%m')} "
                f"from {schema_name}.{table_name}."
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
                f"Successfully appended {len(final_df)} rows for partition {partition_start_date.strftime('%Y-%m')} "
                f"into {schema_name}.{table_name}."
            )
            rows_loaded = len(final_df)
        else:
            context.log.info(
                f"No new data to append for partition {partition_start_date.strftime('%Y-%m')} to {schema_name}.{table_name}."
            )

        return MaterializeResult(
            metadata={
                "table": f"{schema_name}.{table_name}",
                "rows_loaded": rows_loaded,
                "operation": "delete_partition_append",
                "partition": partition_start_date.strftime("%Y-%m"),
                "num_rows": rows_loaded,
                "columns": list(final_df.columns)
                if not final_df.empty
                else target_columns_for_metadata,
                "destination_table": f"{schema_name}.{table_name}",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
                "partition_key": str(context.partition_keys),
                "partition_window_start": partition_start_date.isoformat(),
                "partition_window_end": partition_end_date.isoformat(),
            },
        )
    except Exception as e:
        context.log.error(
            f"Failed to delete/load data for partition {partition_start_date.strftime('%Y-%m')} "
            f"to {schema_name}.{table_name}: {e}"
        )
        raise
