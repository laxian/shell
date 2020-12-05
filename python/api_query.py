#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import requests
import sys
import json


def query(filter, token, index=0):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
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
        ('robotId', filter),
        ('logPath', ''),
        ('logType', ''),
        ('environment', ''),
        ('mapName', ''),
        ('commandStatus', ''),
    )

    response = requests.get(
        'http://${host_part_1}-api.${host_part_2}.com/robot/log/management', headers=headers, params=params)

    if response.status_code == 200:
        try:
            j = json.loads(response.content)
            l = j['data']['list']
            urls = [data['logUrl'] for data in l if data.has_key('logUrl') ]
            return [urls[index]] if index > -1 else urls
        except IOError:
            print('json parse error')
    else:
        print(response.status_code)
    return None


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
        print query(keyword, '${token}', 0)[0]
    except IndexError:
        print('input id pls')
