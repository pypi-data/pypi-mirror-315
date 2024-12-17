import inspect
from datetime import datetime
from typing import Callable

import pandas as pd
from loguru import logger
import os

from ..destination import Destination
from ..source import Source
from ..utils.exceptions import InapplicableTransformation, AdapterConversion

log_level = os.environ.get("LOG_LEVEL") or "DEBUG"
logger.level(log_level)


class Pipeline:

    def __init__(self, pipeline_name: str, source: Source, destination: Destination) -> None:
        self.name = pipeline_name
        self.logger = logger
        self.source = source
        self.destination = destination
        self.transfo: list[Callable[[pd.DataFrame], pd.DataFrame]] = []

    def run(self) -> None:
        starting_time = datetime.now()
        self._info(f"STARTING PIPELINE {self.name}")
        self._debug(f"Starting time {starting_time}")

        self._info(f"LOADING DATA FROM SOURCE {self.source.name} OF TYPE : {self.source.__class__}")
        load_data = self.source.get()
        if load_data is None:
            self._warn("No data found closing pipeline")
            return
        self._debug("Data fetched successfully")

        self._info(f"ADAPTING DATA FROM SOURCE {self.source.name} OF TYPE : {self.source.__class__}")
        data = self.source.adapter(load_data)
        if data is None:
            error_msg = "The source adapter returned no data while data were fetched from the source."
            self._error(error_msg)
            raise AdapterConversion(error_msg)

        self._info("APPLYING CUSTOM FUNCTION TO ADAPTED DATA")
        for transfo in self.transfo:
            try:
                self._debug(f"Data :\n{data.describe()}")
                self._debug(f"Function :\n{inspect.getsource(transfo)}")
                data = transfo(data)
            except BaseException:  # noqa:B036
                error_message = f"Cannot apply custom transformation for function :\n{inspect.getsource(transfo)}"
                self._error(error_message)
                raise InapplicableTransformation(error_message)

        self._info(f"DUMPING DATA TO DESTINATION {self.destination.name} OF TYPE {self.destination.__class__}")
        for d in data:
            self.destination.dump(d)

        self._info("CLOSING PIPELINE")
        ending_time = datetime.now()
        self._debug(f"Ending time : {ending_time}")
        runtime = ending_time - starting_time
        self._debug(f"Runtime : {runtime}")

    def add_transfo(self, transfo: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        self.transfo.append(transfo)

    def _debug(self, msg: str) -> None:
        self.logger.debug(self._enriched_log_msg(msg))

    def _info(self, msg: str) -> None:
        enriched_msg = self._enriched_log_msg(msg)
        upper_msg = enriched_msg.upper()
        spaced_msg = " " + upper_msg + " "
        centered_msg = spaced_msg.center(100, "*")
        self.logger.info(centered_msg)

    def _warn(self, msg: str) -> None:
        self.logger.warning(self._enriched_log_msg(msg))

    def _error(self, msg: str) -> None:
        self.logger.error(self._enriched_log_msg(msg))

    def _enriched_log_msg(self, msg: str) -> str:
        enriched_msg = f"PIPELINE {self.name} - " + msg
        return enriched_msg
