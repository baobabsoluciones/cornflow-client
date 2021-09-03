from abc import ABC, abstractmethod
import json


class MetaInstanceSolution(ABC):
    def __init__(self, data: dict):
        self.data = data

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    @classmethod
    @abstractmethod
    def from_dict(self, data: dict) -> "MetaInstanceSolution":
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def from_json(cls, path: str) -> "MetaInstanceSolution":
        with open(path, "r") as f:
            data_json = json.load(f)
        return cls.from_dict(data_json)

    def to_json(self, path: str) -> None:
        data = self.to_dict()
        with open(path, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    @staticmethod
    @abstractmethod
    def get_schema() -> dict:
        raise NotImplementedError()
