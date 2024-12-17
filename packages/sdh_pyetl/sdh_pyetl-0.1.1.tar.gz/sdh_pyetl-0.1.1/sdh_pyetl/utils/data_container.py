import re
import warnings
from io import BytesIO

import pandas as pd
from pandas import DataFrame


class DataContainer:

    def __init__(self, name: str, data: DataFrame, fmt: str = ""):
        cleaned_name = re.sub(r"[^a-zA-Z0-9]", "_", name)
        normalized_name = re.sub(r"_+", "_", cleaned_name).rstrip("_").lstrip("_")
        self._name = normalized_name.lower()
        if not self._name[0].isalpha():
            warnings.warn(f"The name '{self._name}' does not start with a letter. This may cause issues.", stacklevel=2)
        self._data = self._serialize_data(data)
        self._format = fmt

    @staticmethod
    def _serialize_data(data: DataFrame) -> bytes:
        buffer = BytesIO()
        data.to_parquet(buffer, index=False)
        return buffer.getvalue()

    @staticmethod
    def _deserialize_data(data_bytes: bytes) -> DataFrame:
        buffer = BytesIO(data_bytes)
        return pd.read_parquet(buffer)

    def get_name(self) -> str:
        return self._name

    def get_data(self) -> DataFrame:
        return self._deserialize_data(self._data)

    def get_format(self) -> str | None:
        return None if self._format == "" else self._format
