import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import ms_4_urlp


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса url processor.
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


    def test_01_urlp_read_wiki(self):
        """Тест urlp_read_wiki.
        """
        country_url = ms_4_urlp.urlp_read_wiki(UT_COUNTRY)
        self.assertIsNotNone(country_url)
        self.assertEqual(country_url, UT_COUNTRY_URL)


    def test_02_urlp_write_cache(self):
        """Тест urlp_write_cache.
        """
        flag = ms_4_urlp.urlp_write_cache(UT_COUNTRY, UT_COUNTRY_URL)
        self.assertIsNotNone(flag)
        self.assertEqual(flag, True)


    def test_03_urlp_call_fp(self):
        """Тест urlp_call_fp.
        """
        flag = ms_4_urlp.urlp_call_fp(
            UT_USER_EMAIL, UT_COUNTRY, UT_COUNTRY_URL)
        self.assertIsNotNone(flag)
        self.assertEqual(flag, True)


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)