#!/usr/bin/env python
# coding=utf-8

import sys
import time

from src.log.ore.api_login_ore import raw_login
from src.log.ore.api_query import query_with_retry
from src.log.ore.api_upload import upload_with_retry
from src.log.config import Config
from src.log.utils import *
from src.log.token_exception import TokenException


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
    print('expect: %s' % tick_time_str)
    print('url: %s' % url_time_str)
    return match_time(tick, tock)


def match_time(tick, tock):
    print('tick: %s -> tock: %s' % (tick, tock))
    return -2 < tock - tick <= 10


def get_times(endTime=None):
    """
    endTime: format
    endTime: 1h/1d/1m
    endTime: 2021-01-13_12:00:00
    endTime: None, if None, default 1d; if log_start_time not set, last 24h is set
    """
    config = Config('config.json').config
    log_start_time_f = config['log_start_time']
    now = time.time() -5
    print(now)
    delta = None
    end_time = None

    if not endTime:
        end_time = now
    elif endTime.endswith('d') or endTime.endswith('h') or endTime.endswith('m'):
        if not endTime[:-1].isdigit():
            print('Wrong parameter: %s' % endTime)
            return
        if endTime[-1:] == 'h':
            delta = int(endTime[:-1]) * 60 * 60
        elif endTime[-1:] == 'd':
            delta = int(endTime[:-1]) * 24 * 60 * 60
        elif endTime[-1:] == 'm':
            delta = int(endTime[:-1]) * 30 * 24 * 60 * 60
    else:
        try:
            end_time = int(time.mktime(time.strptime(endTime, '%Y-%m-%d_%H:%M:%S')))
        except Exception as ex:
            print(type(ex))
            print('解析endTime时间异常，请检查格式：%Y-%m-%d_%H:%M:%S')
            return
    if not log_start_time_f:
        # 默认拉取24小时日志
        print('拉取24小时日志')
        if end_time:
            log_start_time = end_time - 24 * 60 * 60
        elif delta:
            end_time = now
            log_start_time = end_time - delta
        else:
            print('error! please set startTime and endTime')
            return
    else:
        print('拉取日志起始点：%s' % log_start_time_f)
        log_start_time = int(time.mktime(time.strptime(log_start_time_f, '%Y-%m-%d_%H:%M:%S')))
        if end_time:
            end_time_f = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(end_time))
            if end_time <= log_start_time:
                print('结束时间不能早于开始时间：%s %s' % (log_start_time_f, end_time_f))
                return
            else:
                print('拉取日志终点：%s' % end_time_f)
        elif delta:
            end_time = log_start_time + delta
            end_time_f = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(end_time))
            print('拉取日志终点：%s' % end_time_f)
            print('delta: %s, end_time: %s, log_start_time: %s' % (delta, end_time, log_start_time))
    return log_start_time, end_time


def schedule(robot_id, path, endTime=None):
    config = Config('config.json').config
    token = config['token_ore'] if 'token_ore' in config else raw_login(
        config['username'], config['password'])
    config['token_ore'] = token

    log_start_time, end_time = get_times(endTime)
    log_start_time *= 1000
    end_time *= 1000
    retry_count = 1
    limit = config['retry_limit']
    # upload
    if upload_with_retry(robot_id, path, log_start_time, token, None, end_time):
        not_found = False
        while True:
            time.sleep(int(config['retry_interval']))
            print('try for %d times' % retry_count)
            query_result = query_with_retry(robot_id, 0)
            if not query_result:
                print('没有查询到url')
                retry_count += 1
                if retry_count > limit:
                    break
                continue
            print(query_result)
            url = query_result[0]
            retry_count += 1
            if match_url(url, end_time/1000):
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
