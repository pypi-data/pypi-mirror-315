from typing import override

from sqlalchemy import create_engine

from . import Destination
from ..utils import DataContainer


class Postgres(Destination):

    def __init__(self, name: str, host: str, port: int, database: str, user: str, schema: str, password: str):
        super().__init__(name)
        self.host = host
        self.port = port
        self.database = database
        self.schema = schema
        self.user = user
        self.password = password
        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode=require"
        )

    @override
    def dump(self, data: DataContainer) -> None:
        table_name = data.get_name()
        df = data.get_data()
        df.to_sql(table_name, self.engine, schema=self.schema, index=False, if_exists="append", method="multi")
