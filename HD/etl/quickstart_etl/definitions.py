import os
from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from quickstart_etl.resources.db_resource import SQLAlchemyResource

from . import assets

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

defs = Definitions(
    resources={
        "sql_alchemy_resource": SQLAlchemyResource(
            conn_str=os.getenv(
                "MSSQL_CONNECTION_STRING", "your_default_dev_string_here"
            )
        ),
    },
    assets=load_assets_from_package_module(assets),
    schedules=[daily_refresh_schedule],
)
