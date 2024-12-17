import os
from typing import override

from ..utils.exceptions import UnsupportedFileType
from . import Destination
from ..utils import DataContainer
from pathlib import Path
import re
import boto3
import tempfile


class s3(Destination):

    def __init__(
        self, name: str, endpoint: str, access_key_id: str, secret_access_key: str, bucket_name: str, folder: str
    ):
        super().__init__(name)
        self.bucket = bucket_name
        self.folder = folder
        url = "https://" + re.sub(r"^(https?://)?", "", endpoint)
        self._s3_client = boto3.client(
            "s3", endpoint_url=url, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
        )
        self._tmp_dirname = Path(tempfile.mkdtemp())

    @override
    def dump(self, data: DataContainer) -> None:
        file_format = data.get_format() if data.get_format() else "csv"
        df = data.get_data()
        df.to_csv(data.get_name() + file_format)

        file_name = data.get_name() + "." + file_format
        output_path = os.path.join(self._tmp_dirname, file_name)
        if file_format == "csv":
            df.to_csv(output_path, sep=";")
        elif file_format == "json":
            df.to_json(output_path)
        elif file_format == "xml":
            df.to_excel(output_path)
        elif file_format == "xlsx":
            df.to_excel(output_path)
        elif file_format == "parquet":
            df.to_parquet(output_path)
        else:
            raise UnsupportedFileType(f"{file_format} format is not supported at the moment.")

        self._s3_client.upload_file(output_path, self.bucket, os.path.join(self.folder, file_name))
