from abc import abstractmethod

from ..utils import DataContainer


class Destination:

    def __init__(self, name: str, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def dump(self, data: DataContainer) -> None:
        raise NotImplementedError

    def set_params(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_params(self) -> dict[str, any]:
        return {key: value for key, value in vars(self).items() if key != "name"}
