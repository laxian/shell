#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import sys
import time

import requests

from .api_login import login_and_save_token
from .config import Config


def upload(robot_id, path, log_start_time, token, env='release', log_end_time=None):
    timestamp = time.time() * 1000 - 5000 if not log_end_time else log_end_time
    print('--------------------------------')
    print(log_end_time)
    print(timestamp)
    print(log_start_time)
    print(token)
    print('--------------------------------')
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36',
        'authToken': token,
        'Origin': 'http://${host_part_1}.${host_part_2}.com',
        'Referer': 'http://${host_part_1}.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"robotId":"%s","environment":"%s","logPath":"%s","startTime":%d,"endTime":%d}' % (
        robot_id, env, path, log_start_time, timestamp)
    print(data)

    response = requests.post('http://${host_part_1}-api.${host_part_2}.com/robot/log/toUploadLog',
                             headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)
        return None


def upload_with_retry(robot_id, path, log_start_time, token=None, env=None, log_end_time=None):
    config = Config('config.json').config
    if not token:
        token = login_and_save_token(config['username'], config['password'])
    if not env:
        env = config['env']
    content = upload(robot_id, path, log_start_time, token, env, log_end_time)
    j = json.loads(content)
    result_code = j.get('resultCode')
    if result_code == 9006:
        print(j['resultDesc'])
        print(u'尝试自动登录...')
        config = Config('config.json').config
        token = login_and_save_token(config['username'], config['password'])
        if token:
            return upload_with_retry(robot_id, path, log_start_time, token, env, log_end_time)
    elif result_code == 9000:
        return content
    else:
        print('other')
        print(j['resultDesc'])


if __name__ == '__main__':
    robot_id = sys.argv[1]
    path = sys.argv[2]
    env = 'release' if len(sys.argv) <= 3 else sys.argv[3]
    token = sys.argv[4] if len(sys.argv) > 4 else Config('config.json').config['token']
    upload_with_retry(robot_id, path, 1590984000000, token, env)
