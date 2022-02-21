from unittest import TestCase
from cornflow_client import CornFlow


class TestCornflowClient(TestCase):
    def setUp(self):
        self.client = CornFlow(url="http://127.0.0.1:5050")

    def tearDown(self):
        pass

    def test_health_endpoint(self):
        response = self.client.is_alive()
        self.assertEqual(response["cornflow_status"], "healthy")
        self.assertEqual(response["airflow_status"], "healthy")
