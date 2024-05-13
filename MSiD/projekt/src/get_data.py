import pandas as pd
from sqlalchemy import create_engine

from src.filter_data import clean_data


def transform_location(location: str):
    if location == "null":
        return None

    return (
        location.replace("ul. ", "")
        .replace("Ul. ", "")
        .replace("Ulica", "")
        .replace(" Wrocław", "")
        .replace(",,", ",")
        + ", Wrocław"
    ).replace(", ,", ",")


def get_data(path: str = "data/data.csv"):
    try:
        dataset = pd.read_csv(path)
        return dataset
    except FileNotFoundError:
        print("File not found, fetching data from database")
        pass

    engine = create_engine(
        "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydb"
    )

    dataset = pd.read_sql_query(
        """SELECT * FROM public."Apartment" WHERE "aiFullResponse" is not NULL AND "area" is not NULL AND "isRoom" = FALSE;
    """,
        engine,
    )

    dataset["numberOfRooms"] = dataset["numberOfRooms"].fillna(
        dataset["aiNumberOfRooms"]
    )

    dataset = dataset.dropna(subset=["aiLocation"])
    dataset["fullLocation"] = dataset["aiLocation"].apply(transform_location)
    dataset = dataset.dropna(subset=["fullLocation"])
    dataset = dataset.drop(
        columns=[
            "updatedAt",
            "aiIsMocked",
            "aiFullResponse",
            "isRoom",
            "cityId",
            "aiLocation",
            "aiNumberOfRooms",
        ]
    )

    return dataset


def get_parsed_data(path: str = "data/data.csv"):
    return clean_data(get_data(path))


if __name__ == "__main__":
    get_data()
