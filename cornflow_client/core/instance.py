from .instance_solution import InstanceSolutionCore
from abc import ABC, abstractmethod


class InstanceCore(InstanceSolutionCore, ABC):
    """
    The instance template.
    """

    @abstractmethod
    def check_inconsistencies(self, *args, **kwargs) -> bool:
        """
        Mandatory method that checks if the problem is feasible for the current instance

        :return: True if the problem is feasible, False otherwise.
        """
        raise NotImplementedError()
