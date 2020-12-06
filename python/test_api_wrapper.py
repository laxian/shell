import unittest

from api_login import login_and_save_token
from api_query import query_with_retry
from api_upload import upload_with_retry
from config import Config


class TestDict(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.config = Config('config.json').config

    def tearDown(self):
        print('tearDown...')

    def test_login_and_save_token(self):
        result = login_and_save_token(self.config['username'], self.config['password'])
        self.assertTrue(result)
        new_config = Config('config.json').config
        self.assertTrue(new_config['token'] == result)

    def test_upload_with_retry(self):
        # token = login(self.config['username'], self.config['password'])
        self.assertTrue(upload_with_retry('GXBOX-${PREFIX}0036', '/sdcard/ex', ''))

    def test_query_with_retry(self):
        # token = login(self.config['username'], self.config['password'])
        query_result = query_with_retry('GXBOX-${PREFIX}0036', '')
        self.assertTrue(isinstance(query_result, list))
        query_result = query_with_retry('GXBOX-${PREFIX}0036', '', 0)
        self.assertEqual(len(query_result), 1)
        self.assertTrue(query_result[0].endswith('.zip'))


if __name__ == '__main__':
    unittest.main()
