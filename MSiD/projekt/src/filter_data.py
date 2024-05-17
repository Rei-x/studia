from pandas import DataFrame


def clean_data(data: DataFrame):
    filtered = data.dropna(subset=["distanceToCityCentre"])

    filtered = filtered.query(
        "400 < price < 10000 and "
        "aiDeposit < 10000 and "
        "distanceToCityCentre < 10000 and "
        "5 < area < 100 and "
        "numberOfRooms > 0"
    )

    return filtered
