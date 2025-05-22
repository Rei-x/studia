from dagster import ConfigurableResource
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class SQLAlchemyResource(ConfigurableResource):
    conn_str: str

    def get_engine(self) -> Engine:
        return create_engine(self.conn_str)
