import os
import sys


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import unittest
from src.log.cli import segway_fetch
from src.log.api_query import query_with_retry
from src.log.utils import get_name
from src.log.cli import segway_download
from src.log.config import Config

class TestDict(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.url = 'http://robot-base.${host_part_2}.com/aws/web/file/download/?bucketName=ota-robot-base&objectKey=log/S1RLM2047C0009_2020-12-04_16-37-27-950_M.zip'
        self.name_expect = 'S1RLM2047C0009_2020-12-04_16-37-27-950_M.zip'
        self.config = Config('config.json').config
        self.timestamp = 1607071047.0

    def tearDown(self):
        print('tearDown...')


    def test_download(self):
        url = query_with_retry('GXBOX-${PREFIX}0036', 0)[0]
        print(url)
        name = get_name(url)
        segway_download(url)
        exit_i = os.system('ls %s' % name)
        self.assertEqual(exit_i, 0)
        os.remove(name)
    
    def test_segway_fetch(self):
        url = query_with_retry('GXBOX-${PREFIX}0036', 0)[0]
        segway_fetch(url)


if __name__ == '__main__':
    unittest.main()
