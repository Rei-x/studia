from dagster import MonthlyPartitionsDefinition


olist_monthly_partitions = MonthlyPartitionsDefinition(
    start_date="2016-09-01",
    end_date="2018-10-01",
    fmt="%Y-%m-%d",
)
