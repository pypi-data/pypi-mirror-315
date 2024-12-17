from abc import abstractmethod
from typing import Generator

from ..utils import DataContainer


class Source:

    def __init__(self, name: str, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def get(self, **kwargs) -> Generator[any]:
        raise NotImplementedError

    @abstractmethod
    def adapter(self, data, **kwargs) -> Generator[DataContainer]:
        raise NotImplementedError

    def set_params(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_params(self) -> dict[str, any]:
        return {key: value for key, value in vars(self).items() if key != "name"}
