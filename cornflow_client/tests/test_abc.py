from cornflow_client.core import MetaInstanceSolution, Application, MetaExperiment
import unittest


class TestABC(unittest.TestCase):
    def test_good_instance(self):
        GoodInstance(dict(a=1))

    def test_bad_instance(self):
        must_fail = lambda: BadInstance(dict(a=1))
        self.assertRaises(TypeError, must_fail)

    def test_experiment(self):
        Experiment(GoodInstance(dict()), GoodInstance(dict()))

    def test_bad_experiment(self):
        must_fail = lambda: BadExmperiment(GoodInstance(dict()), GoodInstance(dict()))
        self.assertRaises(TypeError, must_fail)

    def test_good_application(self):
        GoodApp()

    def test_bad_application(self):
        must_fail = lambda: BadApp()
        self.assertRaises(TypeError, must_fail)


class GoodInstance(MetaInstanceSolution):
    def to_dict(self):
        return self.data

    @classmethod
    def from_dict(cls, data: dict) -> "GoodInstance":
        return cls(data)

    @staticmethod
    def get_schema():
        return dict()


class BadInstance(MetaInstanceSolution):
    @classmethod
    def from_dict(cls, data: dict) -> "BadInstance":
        return cls(data)

    @staticmethod
    def get_schema():
        return dict()


class Experiment(MetaExperiment):
    def solve(self, options: dict):
        raise NotImplementedError()

    def get_objective(self) -> float:
        raise NotImplementedError()

    def get_schema(self) -> dict:
        return dict()

    def check_solution(self, *args, **kwargs) -> dict:
        return dict()


class BadExmperiment(MetaExperiment):
    def solve(self, options) -> float:
        return 1


class GoodApp(Application):
    name = "123"
    instance = GoodInstance
    solvers = dict(default=Experiment)


class BadApp(Application):
    name = "123"
    solvers = dict(default=Experiment)
