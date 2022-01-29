import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
import unittest
import ms_5_fp


################################################################################
# unit-tests
################################################################################

class TestDB(unittest.TestCase):
    """Юнит-тесты для микросервиса file processor.
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

    def test_01_fp_read_wiki(self):
        """Тест fp_read_wiki.
        """
        file_url = ms_5_fp.fp_read_wiki(UT_COUNTRY_URL)
        self.assertIsNotNone(file_url)
        self.assertEqual(file_url, UT_NA_URL)


    def test_02_fp_download_file(self):
        """Тест fp_download_file.
        """
        file_path = os.path.join(os.path.dirname(
            __file__), os.path.basename(UT_NA_URL))
        flag = ms_5_fp.fp_download_file(UT_NA_URL, file_path)
        self.assertIsNotNone(flag)
        self.assertEqual(flag, True)


    def test_03_fp_send_email(self):
        """Тест fp_send_email.
        """
        file_path = os.path.join(os.path.dirname(
            __file__), os.path.basename(UT_NA_URL))
        flag = ms_5_fp.fp_send_email(
            sender = SMTP_SENDER_EMAIL,
            recipient = UT_USER_EMAIL,
            subject = "National anthem: " + UT_COUNTRY,
            content = "See attachments ..",
            attachment = file_path)
        self.assertIsNotNone(flag)
        self.assertEqual(flag, True)


if __name__ == "__main__":
    unittest.main(verbosity = 2, failfast = True)