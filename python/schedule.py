#!/usr/bin/env python
# coding=utf-8

import sys
import time

from config import Config
from api_login import login
from api_query import query
from api_upload import upload
from utils import *


def fetch_and_open(url, app, log_dir='.'):
    # 下载，默认文件名
    download(url)
    name = get_name(url)
    # 解压路径，放在配置的log_dir下面的文件同名目录
    output = '%s/%s' % (log_dir, name.split('.')[0])
    unzip(name, output)
    # 解压后删除压缩包
    os.remove(name)
    # 使用配置的程序打开
    open_with_app(app, output)


def match_url(url, tick):
    """
    :param url: 下载链接
    :param tick: 开始时间
    :return: tick与url上的时间进行匹配，True if match
    """
    if not url:
        return False
    url_time_str = get_time_part(url, r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')
    tok = time.strptime(url_time_str, '%Y-%m-%d_%H-%M-%S')
    tock = time.mktime(tok)
    tick_time_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(tick))
    print('tick: %s' % tick_time_str)
    print('tock: %s' % url_time_str)
    return match_time(tick, tock)


def match_time(tick, tock):
    print('tick: %s -> tock: %s' % (tick, tock))
    return -1 < tock - tick <= 5


def schedule(robot_id, path):
    config = Config('config.json').config
    token = login(config['username'], config['password'])
    config['token'] = token

    # upload
    retry_count = 1
    tick = time.time()
    print(tick)
    limit = config['retry_limit']
    if upload(robot_id, path, token):
        not_found = False
        while True:
            time.sleep(config['retry_interval'])
            print('try for %d times')
            query_result = query(robot_id, token, 0)
            print(query_result)
            url = query_result[0]
            retry_count += 1
            if match_url(url, tick):
                break
            elif retry_count > limit:
                not_found = True
                break
        if not_found:
            print('retry limit exceeded!')
        else:
            fetch_and_open(url, config['open_app'], config['log_dir'])


if __name__ == '__main__':
    robot_id = sys.argv[1]
    path = sys.argv[2]
    schedule(robot_id, path)
