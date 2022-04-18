#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import sys
import time

import requests

from src.log.api_login import login_and_save_token, check_response, clear_token
from src.log.config import Config
from src.log.token_exception import TokenException


def upload(robot_id, path, log_start_time, token, env='release', log_end_time=None):
    timestamp = time.time() * 1000 - 5000 if not log_end_time else log_end_time
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36',
        'authToken': token,
        'Origin': 'http://${host_part_nc}.${host_l}',
        'Referer': 'http://${host_part_nc}.${host_l}/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    url = 'http://${host_part_nc}-api.${host_l}/robot/log/toUploadLog'
    data = '{"robotId":"%s","environment":"%s","logPath":"%s","startTime":%d,"endTime":%d}' % (
        robot_id, env, path, log_start_time, timestamp)
    print('=== === === 开始上传 === === ===')
    print(url)
    print(data)

    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def upload_with_retry(robot_id, path, log_start_time, token=None, env=None, log_end_time=None):
    token = login_and_save_token()
    response = upload(robot_id, path, log_start_time, token, env, log_end_time)
    print(response)
    try:
        response_model = check_response(response)
        print(response_model)
        return response_model
    except TokenException as ex:
        clear_token()
        return upload_with_retry(robot_id, path, log_start_time, token, env, log_end_time)
    except Exception as ex:
        print(type(ex))
        print(response_model)



if __name__ == '__main__':
    robot_id = sys.argv[1]
    path = sys.argv[2]
    # env = 'release' if len(sys.argv) <= 3 else sys.argv[3]
    # token = sys.argv[4] if len(sys.argv) > 4 else Config('config.json').config['token']
    upload_with_retry(robot_id, path, 1590984000000, None, None, None)
