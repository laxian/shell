#!/usr/bin/env python

# -*- coding: UTF-8 -*-


import json

import requests

from .config import Config


def login(username, password):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://${host_part_1}.${host_part_2}.com',
        'Referer': 'http://${host_part_1}.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"username":"%s","password":"%s"}' % (username, password)

    response = requests.post(
        'http://${host_part_1}-api.${host_part_2}.com/user/login', headers=headers, data=data, verify=False)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def login_and_save_token(username, password):
    result = login(username, password)
    if result:
        j = json.loads(result)
        result_code = j.get('resultCode')
        if result_code == 9000:
            token = j['data']['token']
            config = Config('config.json').config
            config['token'] = token
            with open('config.json', 'w') as config_file:
                config_file.write(json.dumps(config))
            return token
        else:
            print(j.get('resultDesc'))


if __name__ == '__main__':
    print(login_and_save_token('${username}', '${password}'))
