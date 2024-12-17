import os
import re
import tempfile
from pathlib import Path
from typing import override, Generator, Union

import boto3
import pandas as pd

from . import Source
from ..utils import DataContainer
from ..utils.exceptions import UnsupportedFileType, UntrustedSource


class S3(Source):

    def __init__(self, endpoint: str, access_key_id: str, secret_access_key: str, bucket_name: str):
        super().__init__()
        self.bucket = bucket_name
        url = "https://" + re.sub(r"^(https?://)?", "", endpoint)
        self._s3_client = boto3.client(
            "s3", endpoint_url=url, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
        )
        self._tmp_dirname = Path(tempfile.mkdtemp())

    @override
    def get(self, incremental: str = None, folder: str = "") -> Generator[Union[str, bytes, os.PathLike]]:
        s3_file_paths = self._list_folder(folder)
        file_names = [os.path.basename(file_path) for file_path in s3_file_paths]
        for file_name, s3_path in zip(file_names, s3_file_paths):
            local_file_path = os.path.join(self._tmp_dirname, file_name)
            self._download_file(s3_path, local_file_path)
            yield local_file_path

    @override
    def adapter(self, data: Generator[Union[str, bytes, os.PathLike]], **kwargs) -> Generator[DataContainer]:
        for d in data:
            file_type = os.path.basename(d).split(".")[-1].lower()
            file_name = os.path.basename(d).split(".")[0].lower()
            if file_type == "csv":
                yield DataContainer(file_name, pd.read_csv(d, header=True, **kwargs), "csv")
            elif file_type == "json":
                yield DataContainer(file_name, pd.read_json(d, **kwargs), "json")
            elif file_type == "html":
                for count, html_data in enumerate(pd.read_html(d, **kwargs)):
                    yield DataContainer(f"{count}_{file_name}", html_data, "html")
            elif file_type == "xml":
                yield DataContainer(file_name, pd.read_xml(d, **kwargs), "xml")
            elif file_type == "xlsx":
                yield DataContainer(file_name, pd.read_excel(d, **kwargs), "xlsx")
            elif file_type == "parquet":
                yield DataContainer(file_name, pd.read_parquet(d, **kwargs), "parquet")
            elif file_type == "pickle":
                raise UntrustedSource("Pickle is not a safe source to use and can lead to security breach.")
            else:
                raise UnsupportedFileType(f"{file_type} format is not supported at the moment.")

    def _list_folder(self, folder) -> list[str]:
        response = self._s3_client.list_objects(Bucket=self.bucket, Prefix=folder)
        if "Contents" not in response.keys():
            return []
        files = [file.get("Key") for file in response.get("Contents") if response.get("Key") != folder]
        return files

    def _download_file(self, target_filename: str, output_filename: str) -> None:
        self._s3_client.download_file(self.bucket, target_filename, output_filename)
