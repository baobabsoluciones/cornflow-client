import json
import os
import time
from unittest import TestCase

from cornflow_client import CornFlow
from cornflow_client.constants import STATUS_OPTIMAL, STATUS_NOT_SOLVED
from cornflow_client.tests.const import PULP_EXAMPLE

path_to_tests_dir = os.path.dirname(os.path.abspath(__file__))


def _load_file(_file):
    with open(_file) as f:
        temp = json.load(f)
    return temp


def _get_file(relative_path):
    return os.path.join(path_to_tests_dir, relative_path)


class TestCornflowClientUser(TestCase):
    def setUp(self):
        self.client = CornFlow(url="http://127.0.0.1:5050/")
        login_result = self.client.login("user", "UserPassword1!")
        self.assertIn("id", login_result.keys())
        self.assertIn("token", login_result.keys())

    def tearDown(self):
        pass

    def test_health_endpoint(self):
        response = self.client.is_alive()
        self.assertEqual(response["cornflow_status"], "healthy")
        self.assertEqual(response["airflow_status"], "healthy")

    def test_sign_up(self):
        response = self.client.sign_up(
            "test_username", "test_username@cornflow.org", "TestPassword2!"
        )
        self.assertIn("id", response.json().keys())
        self.assertIn("token", response.json().keys())
        self.assertEqual(201, response.status_code)

    def test_create_instance(self):
        data = _load_file(PULP_EXAMPLE)
        response = self.client.create_instance(data, "test_example", "test_description")
        items = [
            "id",
            "name",
            "description",
            "created_at",
            "user_id",
            "data_hash",
            "schema",
            "executions",
        ]
        for item in items:
            self.assertIn(item, response.keys())

        self.assertEqual("test_example", response["name"])
        self.assertEqual("solve_model_dag", response["schema"])
        self.assertEqual("test_description", response["description"])

        return response

    def test_create_case(self):
        data = _load_file(PULP_EXAMPLE)
        response = self.client.create_case(
            name="test_case",
            schema="solve_model_dag",
            data=data,
            description="test_description",
        )

        items = [
            "id",
            "name",
            "description",
            "created_at",
            "user_id",
            "data_hash",
            "schema",
            "solution_hash",
            "path",
            "updated_at",
            "is_dir",
        ]
        print(f"Create case response has keys: {response.keys()}")

        for item in items:
            self.assertIn(item, response.keys())
        self.assertEqual("test_case", response["name"])
        self.assertEqual("solve_model_dag", response["schema"])
        self.assertEqual("test_description", response["description"])

    def test_create_instance_file(self):
        response = self.client.create_instance_file(
            _get_file("../data/test_mps.mps"),
            name="test_filename",
            description="filename_description",
        )

        items = [
            "id",
            "name",
            "description",
            "created_at",
            "user_id",
            "data_hash",
            "schema",
            "executions",
        ]

        for item in items:
            self.assertIn(item, response.keys())

        self.assertEqual("test_filename", response["name"])
        self.assertEqual("solve_model_dag", response["schema"])
        self.assertEqual("filename_description", response["description"])

    def test_create_execution(self):
        instance = self.test_create_instance()
        response = self.client.create_execution(
            instance_id=instance["id"],
            config={"solver": "PULP_CBC_CMD", "timeLimit": 60},
            name="test_execution",
            description="execution_description",
            schema="solve_model_dag",
        )
        items = [
            "id",
            "name",
            "description",
            "created_at",
            "user_id",
            "data_hash",
            "schema",
            "config",
            "instance_id",
            "state",
            "message",
        ]

        for item in items:
            self.assertIn(item, response.keys())

        self.assertEqual(instance["id"], response["instance_id"])
        self.assertEqual("test_execution", response["name"])
        self.assertEqual("execution_description", response["description"])
        self.assertEqual(
            {"solver": "PULP_CBC_CMD", "timeLimit": 60}, response["config"]
        )
        self.assertEqual(STATUS_NOT_SOLVED, response["state"])

        return response

    def test_execution_results(self):
        execution = self.test_create_execution()
        time.sleep(15)
        response = self.client.get_results(execution["id"])

        items = [
            "id",
            "name",
            "description",
            "created_at",
            "user_id",
            "data_hash",
            "schema",
            "config",
            "instance_id",
            "state",
            "message",
        ]

        for item in items:
            self.assertIn(item, response.keys())

        self.assertEqual(execution["id"], response["id"])
        self.assertEqual(STATUS_OPTIMAL, response["state"])

    def test_execution_status(self):
        pass

    def test_create_case_execution(self):
        execution = self.test_create_execution()
        pass

    def test_stop_execution(self):
        execution = self.test_create_execution()
        response = self.client.stop_execution(execution["id"])
        self.assertEqual(response["message"], "The execution has been stopped")

    def test_get_execution_log(self):
        pass

    def test_get_execution_solution(self):
        pass

    def test_get_all_instances(self):
        instance1 = self.test_create_instance()
        instance2 = self.test_create_instance()
        pass

    def test_get_all_executions(self):
        pass

    def test_get_one_user(self):
        pass

    def test_get_one_instance(self):
        pass

    def test_get_one_case(self):
        pass

    def test_delete_one_case(self):
        pass

    def test_put_one_case(self):
        pass

    def test_path_one_case(self):
        pass

    def test_delete_one_instance(self):
        pass

    def test_get_schema(self):
        pass

    def test_get_all_schemas(self):
        pass


class TestCornflowClientAdmin(TestCase):
    def setUp(self):
        self.client = CornFlow(url="http://127.0.0.1:5050/")
        login_result = self.client.login("admin", "Adminpassword1!")
        self.assertIn("id", login_result.keys())
        self.assertIn("token", login_result.keys())

    def tearDown(self):
        pass

    def test_get_all_users(self):
        pass

    def test_get_one_user(self):
        pass


class TestCornflowClientService(TestCase):
    def setUp(self):
        self.client = CornFlow(url="http://127.0.0.1:5050/")
        login_result = self.client.login("airflow", "Airflow_test_password1")
        self.assertIn("id", login_result.keys())
        self.assertIn("token", login_result.keys())

    def tearDown(self):
        pass

    def test_get_execution_data(self):
        pass

    def test_write_execution_solution(self):
        pass

    def test_get_deployed_dags(self):
        pass

    def test_post_deployed_dag(self):
        pass
