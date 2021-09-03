from typing import Type, Dict
from timeit import default_timer as timer
from .instance_solution import MetaInstanceSolution
from .experiment import MetaExperiment
from abc import ABC, abstractmethod
from cornflow_client.constants import (
    STATUS_OPTIMAL,
    STATUS_NOT_SOLVED,
    STATUS_INFEASIBLE,
    STATUS_UNDEFINED,
    STATUS_TIME_LIMIT,
    SOLUTION_STATUS_FEASIBLE,
    SOLUTION_STATUS_INFEASIBLE,
)


class Application(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def instance(self) -> Type[MetaInstanceSolution]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def solvers(self) -> Dict[str, Type[MetaExperiment]]:
        raise NotImplementedError()

    def solve(self, data: dict, config: dict):
        """
        :param data: json for the problem
        :param config: execution configuration, including solver
        :return: solution and log
        """
        print("Solving the model")
        solver = config.get("solver", "default")
        solver_class = self.get_solver(name=solver)
        if solver_class is None:
            raise NoSolverException("Solver {} is not available".format(solver))
        inst = self.instance.from_dict(data)
        algo = solver_class(inst, None)
        start = timer()

        try:
            status = algo.solve(config)
            print("ok")
        except Exception as e:
            print("problem was not solved")
            print(e)
            status = 0

        sol = None  # export everything:
        status_conv = {
            STATUS_OPTIMAL: "Optimal",
            STATUS_TIME_LIMIT: "Time limit",
            STATUS_INFEASIBLE: "Infeasible",
            STATUS_UNDEFINED: "Unknown",
            STATUS_NOT_SOLVED: "Not solved",
        }
        log = dict(
            time=timer() - start,
            solver=solver,
            status=status_conv.get(status, "Unknown"),
            status_code=status,
            sol_code=SOLUTION_STATUS_INFEASIBLE,
        )
        # check if there is a solution
        if algo.solution is not None and len(algo.solution.data):
            sol = algo.solution.to_dict()
            log["sol_code"] = SOLUTION_STATUS_FEASIBLE
        return sol, "", log

    def get_solver(self, name: str = "default") -> Type[MetaExperiment]:
        return self.solvers.get(name)


class NoSolverException(Exception):
    pass
