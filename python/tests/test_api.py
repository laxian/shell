import unittest

import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from src.log.api_login import login
from src.log.api_query import query_with_retry
from src.log.api_upload import upload_with_retry
from src.log.config import Config


class TestDict(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.url = 'http://robot-base.${host_part_2}.com/aws/web/file/download/?bucketName=ota-robot-base&objectKey=log/GXBOX' \
                   '-${PREFIX}0036_2020-12-05_23-06-05-137_M.zip '
        self.name_expect = 'GXBOX-${PREFIX}0036_2020-12-05_23-06-05-137_M.zip'
        self.config = Config('config.json').config
        self.timestamp = 1607180765.0

    def tearDown(self):
        print('tearDown...')

    def test_login(self):
        login_result = login(self.config['username'], self.config['password'])
        print(login_result)
        self.assertTrue(login_result)

    def test_upload(self):
        token = login(self.config['username'], self.config['password'])
        self.assertTrue(upload_with_retry('GXBOX-${PREFIX}0036', '/sdcard/ex', token))

    def test_query(self):
        # token = login(self.config['username'], self.config['password'])
        query_result = query_with_retry('GXBOX-${PREFIX}0036', '78cf8dfc533e48369cc3c0a1bcdfb6ee')
        self.assertTrue(isinstance(query_result, list))
        query_result = query_with_retry('GXBOX-${PREFIX}0036', '78cf8dfc533e48369cc3c0a1bcdfb6ee', 0)
        self.assertEqual(len(query_result), 1)
        self.assertTrue(query_result[0].endswith('.zip'))


if __name__ == '__main__':
    unittest.main()
