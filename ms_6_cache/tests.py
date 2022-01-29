import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import requests


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса cache.
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
        response = requests.post(MS_CACHE_URL + "/clear_all")
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


    def test_02_set_country(self):
        """Тест /set_country.
        """
        params  = {"country": UT_COUNTRY, "country_url": UT_COUNTRY_URL}
        response = requests.post(MS_CACHE_URL + "/set_country", json = params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


    def test_03_get_country(self):
        """Тест /get_country.
        """
        params  = {"country": UT_COUNTRY}
        response = requests.post(MS_CACHE_URL + "/get_country", json = params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertIn("url", data)
        self.assertEqual(data["status_code"], "0")
        self.assertEqual(data["url"], UT_COUNTRY_URL)

    def test_04_proc_country(self):
        """Тест /proc_country.
        """
        params  = {"country": UT_COUNTRY, "country_url": UT_COUNTRY_URL}
        response = requests.post(MS_CACHE_URL + "/proc_country", json = params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)