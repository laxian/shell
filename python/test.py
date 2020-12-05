import os
import unittest

import time

from api_login import login
from api_query import query
from api_upload import upload
from config import Config
from schedule import match_url, schedule, match_time
from utils import get_name, download, unzip, open_with_app, get_time_part


class TestDict(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.url = 'http://robot-base.${host_part_2}.com/aws/web/file/download/?bucketName=ota-robot-base&objectKey=log/GXBOX-${PREFIX}0036_2020-12-05_23-06-05-137_M.zip'
        self.name_expect = 'GXBOX-${PREFIX}0036_2020-12-05_23-06-05-137_M.zip'
        self.config = Config('config.json').config
        self.timestamp = 1607180765.0


    def tearDown(self):
        print('tearDown...')

    def test_login(self):
        login_result = login(self.config['username'], self.config['password'])
        print (login_result)
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

    def test_config(self):
        self.assertTrue(self.config.has_key('username'))
        self.assertTrue(self.config.has_key('password'))
        self.assertTrue(self.config.has_key('token'))
        self.assertTrue(self.config.has_key('env'))
        self.assertTrue(self.config.has_key('open_app'))
        self.assertTrue(self.config.has_key('retry_limit'))
        self.assertTrue(self.config.has_key('retry_interval'))

    def test_utils_get_name(self):
        name_result = get_name(self.url)
        self.assertEqual(name_result, self.name_expect)

    def test_utils_download(self):
        download(self.url)
        exit_i = os.system('ls %s' % self.name_expect)
        self.assertEqual(exit_i, 0)
        os.remove(self.name_expect)

    def test_utils_unzip(self):
        download(self.url)
        output = 'test_unzip'
        unzip(self.name_expect, output)
        exit_i = os.system('ls %s' % output)
        self.assertEqual(exit_i, 0)
        os.remove(self.name_expect)
        os.system('rm -rf %s' % output)

    def test_utils_open_with_app(self):
        result = open_with_app('code', '.')
        self.assertEqual(result, 0)

    def test_utils_get_time_part(self):
        time_part = get_time_part(self.url, r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}')
        self.assertTrue(time_part)

    def test_schedule_match_url(self):
        tick = self.timestamp
        self.assertTrue(match_url(self.url, tick))

        t1 = time.mktime(time.strptime('2020-12-05_11-12-59', '%Y-%m-%d_%H-%M-%S'))
        url = 'http://xxxx_2020-12-05_11-13-04-033_M.zip'
        url2 = 'http://xxxx_2020-12-05_11-13-05-033_M.zip'
        url3 = 'http://xxxx_2020-12-05_11-12-59-033_M.zip'
        url4 = 'http://xxxx_2020-12-05_11-12-58-033_M.zip'
        self.assertTrue(match_url(url, t1))
        self.assertFalse(match_url(url2, t1))
        self.assertTrue(match_url(url3, t1))
        self.assertFalse(match_url(url4, t1))

    def test_schedule_match_time(self):
        t1 = time.mktime(time.strptime('2020-12-05_11-12-59', '%Y-%m-%d_%H-%M-%S'))
        t2 = time.mktime(time.strptime('2020-12-05_11-13-04', '%Y-%m-%d_%H-%M-%S'))
        t3 = time.mktime(time.strptime('2020-12-05_11-13-05', '%Y-%m-%d_%H-%M-%S'))
        self.assertTrue(match_time(t1, t2))
        self.assertTrue(match_time(t1, t1))
        self.assertFalse(match_time(t1, t3))


    def test_schedule_schedule(self):
        schedule('GXBOX-${PREFIX}0036', 'sdcard/ex')


if __name__ == '__main__':
    unittest.main()
