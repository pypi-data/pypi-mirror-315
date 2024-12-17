from pydantic import BaseModel


class S3Config(BaseModel):
    endpoint: str
    access_key_id: str
    secret_access_key: str
    bucket_name: str
