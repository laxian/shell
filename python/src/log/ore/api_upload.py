#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import sys
import time

import requests

from src.log.ore.api_login_ore import login_and_save_token, check_response, clear_token
from src.log.config import Config
from src.log.token_exception import TokenException


def upload(robot_id, path, log_start_time, token, env='release', log_end_time=None):
    timestamp = time.time() * 1000 - 5000 if not log_end_time else log_end_time
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7,th;q=0.6,de-DE;q=0.5,de;q=0.4,nl;q=0.3,fr-FR;q=0.2,fr;q=0.1',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://navcenter-oregon.${host_l}',
        'Referer': 'https://navcenter-oregon.${host_l}/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'authToken': token,
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'x-requested-with': 'XMLHttpRequest',
    }

    url = 'http://${host_part_nc}-api-oregon.${host_l}/robot/log/toUploadLog'
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
    # token = sys.argv[4] if len(sys.argv) > 4 else Config('config.json').config['token_ore']
    upload_with_retry(robot_id, path, 1590984000000, None, None, None)
