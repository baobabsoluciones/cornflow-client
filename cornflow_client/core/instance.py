from .instance_solution import InstanceSolutionCore
from abc import ABC, abstractmethod


class InstanceCore(InstanceSolutionCore, ABC):
    """
    The instance template.
    """

    def check_inconsistencies(self, *args, **kwargs) -> dict:
        """
        Method that checks if there are inconsistencies in the data of the current instance.

        :return: A dictionary containing the inconsistencies found.
        """
        return dict()
