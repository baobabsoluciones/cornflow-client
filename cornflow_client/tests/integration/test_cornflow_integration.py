import json
import os
from unittest import TestCase

from cornflow_client import CornFlow
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
        for it in items:
            self.assertIn(it, response.keys())

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
            "dependents",
            "is_dir",
        ]

        for it in items:
            self.assertIn(it, response.keys())
        self.assertEqual("test_case", response["name"])
        self.assertEqual("solve_model_dag", response["schema"])
        self.assertEqual("test_description", response["description"])

    def test_create_instance_file(self):
        response = self.client.create_instance_file(
            _get_file("./data/test_mps.mps"),
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

        for it in items:
            self.assertIn(it, response.keys())

        self.assertEqual("test_filename", response["name"])
        self.assertEqual("solve_model_dag", response["schema"])
        self.assertEqual("filename_description", response["description"])

    def test_create_execution(self):
        instance = self.test_create_instance()
        return True

    def test_create_full_case(self):
        pass

    def test_get_execution_data(self):
        execution = self.test_create_execution()
        pass

    def test_stop_execution(self):
        pass

    def test_execution_results(self):
        pass

    def test_execution_status(self):
        pass

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

    def test_get_deployed_dags(self):
        pass

    def test_post_deployed_dag(self):
        pass
