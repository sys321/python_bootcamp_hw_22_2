import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import requests


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса user interface.
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


    def test_01_proc_request(self):
        """Тест /proc_request.
        """
        query = {"email": UT_USER_EMAIL, "country": UT_COUNTRY}
        response = requests.post(MS_UI_URL + "/proc_request", json = query)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertIn("status_code", data)
        self.assertIn("status_message", data)
        self.assertEqual(data["status_code"], "0")


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)