from unittest import TestCase

from cornflow_client.airflow.api import Airflow


class TestAirflowClient(TestCase):
    def setUp(self):
        self.client = Airflow(url="http://127.0.0.1:8080", user="admin", pwd="admin")

    def test_alive(self):
        self.assertTrue(self.client.is_alive())

    def test_connect_from_config(self):
        client = Airflow.from_config(
            {
                "AIRFLOW_URL": "http://127.0.0.1:8080",
                "AIRFLOW_USER": "admin",
                "AIRFLOW_PWD": "admin",
            }
        )
        self.assertTrue(client.is_alive())

    def test_bad_connection(self):
        client = Airflow(url="http://127.0.0.1:8080", user="admin", pwd="admin!")
        self.assertFalse(client.is_alive())
