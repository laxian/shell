#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import sys

import requests

from src.log.ore.api_login_ore import login_and_save_token, check_response, clear_token
from src.log.config import Config
from src.log.token_exception import TokenException


def raw_query(key, token):
    """
    查询，返回json
    :param key:
    :param token:
    :return:
    """
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7,th;q=0.6,de-DE;q=0.5,de;q=0.4,nl;q=0.3,fr-FR;q=0.2,fr;q=0.1',
        'Connection': 'keep-alive',
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

    print('=== === === 开始查询 === === ===')
    url = 'http://${host_part_nc}-api-oregon.${host_l}/robot/log/management'
    print(url)
    print("token %s, params %r" % (token, params))

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)
    return None


def query_with_retry(key, index=-1):
    token = login_and_save_token()
    response = raw_query(key, token)
    try:
        j = check_response(response)
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
    except TokenException as ex:
        clear_token()
        return query_with_retry(key, index)
    except Exception as ex:
        print(type(ex))
        print(j)


def query_model_with_retry(key, index=-1):
    token = login_and_save_token()
    response = raw_query(key, token)
    try:
        j = check_response(response)
        print(j)
        if 'list' in j['data']:
            return j['data']['list']
        else:
            return None
    except TokenException as ex:
        clear_token()
        return query_model_with_retry(key, index)
    except Exception as ex:
        print(type(ex))
        print(j)


if __name__ == '__main__':
    key = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else Config('config.json').config['token_ore']
    index = 0
    query_with_retry(key, index)
