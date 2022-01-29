import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import requests


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса message broker.
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


    def test_01_call_urlp(self):
        """Тест /call_urlp.
        """
        query = {"email": UT_USER_EMAIL, "country": UT_COUNTRY}
        response = requests.post(MS_MB_URL + "/call_urlp", json = query)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


    def test_02_call_fp(self):
        """Тест /call_fp.
        """
        query = {"email": UT_USER_EMAIL, "country": UT_COUNTRY, "country_url": UT_COUNTRY_URL}
        response = requests.post(MS_MB_URL + "/call_fp", json = query)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)