#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import sys

import requests

from .api_login import login_and_save_token
from .config import Config


def _query(key, token):
    """
    查询，返回json
    :param key:
    :param token:
    :return:
    """
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36',
        'authToken': token,
        'Origin': 'http://${host_part_1}.${host_part_2}.com',
        'Referer': 'http://${host_part_1}.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('page', '1'),
        ('pageSize', '10'),
        ('startCreateTime', ''),
        ('endCreateTime', ''),
        ('robotId', key),
        ('logPath', ''),
        ('logType', ''),
        ('environment', ''),
        ('mapName', ''),
        ('commandStatus', ''),
    )

    response = requests.get(
        'http://${host_part_1}-api.${host_part_2}.com/robot/log/management', headers=headers, params=params)

    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)
    return None


def query_model_with_token_retry(key, token, index=-1):
    result = _query(key, token)
    if result:
        j = json.loads(result)
        result_code = j.get('resultCode')
        if j.get('resultCode') == 9000:
            if 'list' in j['data']:
                return j['data']['list']
            else:
                return None
        elif result_code == 9006:
            print(j.get('resultDesc'))
            print(u'尝试自动登录...')
            config = Config('config.json').config
            token = login_and_save_token(config['username'], config['password'])
            if token:
                return query_model_with_token_retry(key, token, index)
        else:
            print(j.get('resultDesc'))
    else:
        pass


def query_with_token_retry(key, token, index=-1):
    result = _query(key, token)
    if result:
        j = json.loads(result)
        result_code = j.get('resultCode')
        if j.get('resultCode') == 9000:
            if 'list' in j['data']:
                list_part = j['data']['list']
                urls = [data['logUrl'] for data in list_part if 'logUrl' in data]
                if urls:
                    url = [urls[index]] if index > -1 else urls
                else:
                    return None
                return url
            else:
                return None
        elif result_code == 9006:
            print(j.get('resultDesc'))
            print(u'尝试自动登录...')
            config = Config('config.json').config
            token = login_and_save_token(config['username'], config['password'])
            if token:
                return query_with_token_retry(key, token, index)
        else:
            print(j.get('resultDesc'))
    else:
        pass


def query_with_retry(key, index=-1):
    config = Config('config.json').config
    token = config['token']
    if not token:
        if config['username'] and config['password']:
            token = login_and_save_token(config['username'], config['password'])
        else:
            print('未设置账户密码')
            return
    return query_with_token_retry(key, token, index)


def query_model_with_retry(key, index=-1):
    config = Config('config.json').config
    token = config['token']
    if not token:
        if config['username'] and config['password']:
            token = login_and_save_token(config['username'], config['password'])
        else:
            print('未设置账户密码')
            return
    return query_model_with_token_retry(key, token, index)


if __name__ == '__main__':
    key = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else Config('config.json').config['token']
    index = 0
    query_with_token_retry(key, token, index)
