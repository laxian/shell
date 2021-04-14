import os
import sys
import unittest


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from src.log.api_upload import upload_with_retry
from src.log.api_login import login_and_save_token
from src.log.api_query import query_with_token_retry
from src.log.config import Config


class TestDict(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.config = Config('config.json').config

    def tearDown(self):
        print('tearDown...')

    def test_login_and_save_token(self):
        result = login_and_save_token(self.config['username'], self.config['password'])
        new_config = Config('config.json').config
        self.assertTrue(result)
        self.assertTrue(new_config['token'] == result)

    def test_upload_with_retry(self):
        # token = login(self.config['username'], self.config['password'])
        self.assertTrue(upload_with_retry('GXBOX-${PREFIX}0036', '/sdcard/ex', ''))

    def test_query_with_retry(self):
        # token = login(self.config['username'], self.config['password'])
        query_result = query_with_token_retry('GXBOX-${PREFIX}0036', '')
        self.assertTrue(isinstance(query_result, list))
        query_result = query_with_token_retry('GXBOX-${PREFIX}0036', '', 0)
        self.assertEqual(len(query_result), 1)
        self.assertTrue(query_result[0].endswith('.zip'))


if __name__ == '__main__':
    unittest.main()
