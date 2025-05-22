# olist_etl/partitions.py
from dagster import MonthlyPartitionsDefinition

# Adjust start_date based on your earliest order_purchase_timestamp
# For Olist, it's around September 2016.
# Dagster will generate partitions up to the current month by default if end_date is not specified.
olist_monthly_partitions = MonthlyPartitionsDefinition(
    start_date="2016-09-01",  # Example, adjust to your data's min date
    end_date="2018-10-01",
    fmt="%Y-%m-%d",  # Using full date format for partition keys, easier for date comparisons
    # Alternatively, "%Y-%m" for month string keys
)
