from dagster import AssetExecutionContext, Output, RetryPolicy
import pandas as pd
from sqlalchemy import Engine, inspect, text


def _prepare_df_for_load(
    context: AssetExecutionContext,
    df_merged: pd.DataFrame,
    target_columns: list[str],
    business_key_column: str | None = None,
) -> pd.DataFrame:
    final_df = pd.DataFrame(columns=target_columns)
    for col in target_columns:
        if col in df_merged.columns:
            final_df[col] = df_merged[col]
        else:
            context.log.warning(
                f"Target column '{col}' not found in merged DataFrame. Filling with NA."
            )
            final_df[col] = pd.NA

    if business_key_column:
        rows_before_dropna = len(final_df)
        final_df = final_df.dropna(subset=[business_key_column])
        rows_after_dropna = len(final_df)
        if rows_before_dropna > rows_after_dropna:
            context.log.warning(
                f"Dropped {rows_before_dropna - rows_after_dropna} rows due to missing business key '{business_key_column}'."
            )
    return final_df


def _upsert_to_db_via_staging(
    context: AssetExecutionContext,
    engine: Engine,
    df_to_load: pd.DataFrame,
    target_table_name: str,
    target_schema_name: str,
    business_key_cols: list[str],
    all_target_cols_for_df: list[str],
) -> Output[dict]:
    if df_to_load.empty:
        context.log.info(
            f"No data to upsert into {target_schema_name}.{target_table_name}."
        )
        return Output(
            value={
                "table": f"{target_schema_name}.{target_table_name}",
                "rows_inserted": 0,
                "rows_updated": 0,
                "operation": "upsert_skipped_empty_df",
            },
            metadata={
                "num_rows_processed_in_df": 0,
                "columns": all_target_cols_for_df,
                "destination_table": f"{target_schema_name}.{target_table_name}",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
            },
        )

    # More unique staging table name to minimize potential clashes if runs overlap slightly
    # and cleanup fails, though concurrency control is the primary fix for deadlocks.
    run_id_prefix = context.run_id.split("-")[0]  # Short prefix from run_id
    staging_table_name = f"stg_{target_table_name}_{run_id_prefix}_{pd.Timestamp.now().strftime('%H%M%S%f')}".lower()

    rows_affected_by_merge = 0

    try:
        with engine.connect() as connection:
            # Check if staging table exists and drop it explicitly first to reduce to_sql's internal reflection work
            # This is a small optimization, the main fix is concurrency control.
            inspector = inspect(connection)
            if inspector.has_table(staging_table_name, schema=target_schema_name):
                context.log.info(
                    f"Dropping existing staging table {target_schema_name}.{staging_table_name}"
                )
                connection.execute(
                    text(f"DROP TABLE {target_schema_name}.{staging_table_name}")
                )
                # No commit needed for DROP TABLE usually, or it's part of the transaction

            df_to_load.to_sql(
                name=staging_table_name,
                con=connection,
                schema=target_schema_name,
                index=False,
                chunksize=1000,
            )
            context.log.info(
                f"Loaded {len(df_to_load)} rows into staging table {target_schema_name}.{staging_table_name}."
            )

            update_set_clauses = [
                f"Target.{col} = Source.{col}"
                for col in all_target_cols_for_df
                if col not in business_key_cols
            ]
            insert_cols_target = ", ".join(all_target_cols_for_df)
            insert_cols_source = ", ".join(
                [f"Source.{col}" for col in all_target_cols_for_df]
            )
            join_conditions = " AND ".join(
                [f"Target.{bk} = Source.{bk}" for bk in business_key_cols]
            )

            simple_merge_sql = f"""
            MERGE {target_schema_name}.{target_table_name} AS Target
            USING {target_schema_name}.{staging_table_name} AS Source
            ON ({join_conditions})
            WHEN MATCHED THEN
                UPDATE SET {", ".join(update_set_clauses)}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insert_cols_target})
                VALUES ({insert_cols_source});
            """

            result = connection.execute(text(simple_merge_sql))
            rows_affected_by_merge = result.rowcount if result else 0
            context.log.info(
                f"Successfully executed MERGE into {target_schema_name}.{target_table_name}. Affected rows: {rows_affected_by_merge}"
            )

            connection.execute(
                text(f"DROP TABLE {target_schema_name}.{staging_table_name}")
            )
            connection.commit()  # Commit all operations: staging load, merge, staging drop
            context.log.info(
                f"Dropped staging table {target_schema_name}.{staging_table_name} and committed transaction."
            )

        return Output(
            value={
                "table": f"{target_schema_name}.{target_table_name}",
                "rows_affected_by_merge": rows_affected_by_merge,
                "operation": "upsert_via_staging",
            },
            metadata={
                "num_rows_processed_in_df": len(df_to_load),
                "columns": all_target_cols_for_df,
                "destination_table": f"{target_schema_name}.{target_table_name}",
                "source": "olist_dwh",
                "load_time": pd.Timestamp.now().isoformat(),
            },
        )
    except Exception as e:
        context.log.error(
            f"Failed to upsert data to {target_schema_name}.{target_table_name}: {e}"
        )
        # Attempt to drop staging table on error if it exists (outside the transaction that might have rolled back)
        try:
            with engine.connect() as conn_cleanup:  # New connection for cleanup
                inspector = inspect(conn_cleanup)
                if inspector.has_table(staging_table_name, schema=target_schema_name):
                    conn_cleanup.execute(
                        text(f"DROP TABLE {target_schema_name}.{staging_table_name}")
                    )
                    conn_cleanup.commit()
                    context.log.info(
                        f"Cleaned up staging table {target_schema_name}.{staging_table_name} after error."
                    )
        except Exception as cleanup_e:
            context.log.error(
                f"Failed to cleanup staging table {target_schema_name}.{staging_table_name}: {cleanup_e}"
            )
        raise


# --- Dimension Loader Assets ---
# Define a common retry policy and concurrency tag
DIM_LOADER_RETRY_POLICY = RetryPolicy(
    max_retries=2, delay=60
)  # Retry 2 times, 60s delay
DIM_LOADER_CONCURRENCY_TAGS = {
    "dagster/concurrency_key": "mssql_dimension_upsert",
    "dagster/max_concurrent_runs": "1",
}
