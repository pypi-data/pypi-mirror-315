from pydantic import BaseModel


class PostgresConfig(BaseModel):
    name: str
    host: str
    port: int
    database: str
    user: str
    db_schema: str
    password: str
