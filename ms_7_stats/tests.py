import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import requests
import ms_7_stats


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса stats.
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


    def test_01_stats_read_data(self):
        """Тест stats_read_data.
        """
        pass


    def test_02_stats_gen_report(self):
        """Тест stats_gen_report.
        """
        pass


    def test_03_stats_send_email(self):
        """Тест stats_send_email.
        """
        pass


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)