import unittest

from api_login import login
from api_query import query
from api_upload import upload
from config import Config


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
        self.assertTrue(upload('GXBOX-${PREFIX}0036', '/sdcard/ex', token))

    def test_query(self):
        # token = login(self.config['username'], self.config['password'])
        query_result = query('GXBOX-${PREFIX}0036', '78cf8dfc533e48369cc3c0a1bcdfb6ee')
        self.assertTrue(isinstance(query_result, list))
        self.assertEqual(len(query_result), 1)
        self.assertTrue(query_result[0].endswith('.zip'))


if __name__ == '__main__':
    unittest.main()
