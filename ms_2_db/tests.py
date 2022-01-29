import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import requests


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса database.
    """

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_01_clear_all(self):
        """Тест /clear_all.
        """
        response = requests.post(MS_DB_URL + "/clear_all")
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


    def test_02_create_user(self):
        """Тест /create_user.
        """
        user = {"email": UT_USER_EMAIL}
        response = requests.post(MS_DB_URL + "/create_user", json = user)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertIn("data", data)
        self.assertEqual(data["status_code"], "0")

        # double
        user = {"email": UT_USER_EMAIL}
        response = requests.post(MS_DB_URL + "/create_user", json = user)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "1")


    def test_03_create_subscriber(self):
        """Тест /create_subscriber.
        """
        subscriber = {"email": UT_SUBSCRIBER_EMAIL}
        response = requests.post(MS_DB_URL + "/create_subscriber", json = subscriber)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertIn("data", data)
        self.assertEqual(data["status_code"], "0")

        # double
        subscriber = {"email": UT_SUBSCRIBER_EMAIL}
        response = requests.post(MS_DB_URL + "/create_subscriber", json = subscriber)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "1")


    def test_04_journalize_request(self):
        """Тест /journalize_request.
        """
        request = {"email": UT_USER_EMAIL, "country": UT_COUNTRY}
        response = requests.post(MS_DB_URL + "/journalize_request", json = request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


    def test_05_stats_data(self):
        """Тест /stats_data.
        """
        response = requests.post(MS_DB_URL + "/stats_data")
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertIn("data", data)
        self.assertEqual(data["status_code"], "0")


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)