from abc import ABC, abstractmethod
from .instance_solution import MetaInstanceSolution
from typing import Type, Union
from cornflow_client.constants import STATUS_NOT_SOLVED, SOLUTION_STATUS_INFEASIBLE


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
    def instance(self, value: MetaInstanceSolution) -> None:
        self._instance = value

    @property
    def solution(self) -> MetaInstanceSolution:
        return self._solution

    @solution.setter
    def solution(self, value: MetaInstanceSolution) -> None:
        self._solution = value

    @abstractmethod
    def solve(self, options: dict) -> dict:
        pass

    @abstractmethod
    def get_objective(self) -> float:
        pass

    @abstractmethod
    def check_solution(self, *args, **kwargs) -> dict:
        pass
