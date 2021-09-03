from abc import ABC, abstractmethod
from .instance_solution import MetaInstanceSolution
from typing import Type, Union


class MetaExperiment(ABC):
    def __init__(
        self,
        instance: MetaInstanceSolution,
        solution: Union[MetaInstanceSolution, None] = None,
    ):
        self.instance = instance
        self.solution = solution

    @property
    def instance(self) -> MetaInstanceSolution:
        return self._instance

    @instance.setter
    def instance(self, value: MetaInstanceSolution):
        self._instance = value

    @abstractmethod
    def solve(self, options: dict) -> int:
        pass

    @abstractmethod
    def get_objective(self) -> float:
        pass

    @abstractmethod
    def check_solution(self, *args, **kwargs) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_schema() -> dict:
        """
        returns the configuration schema for the solve() method
        """
        pass
