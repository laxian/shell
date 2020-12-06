#!/usr/bin/env python

# -*- coding: UTF-8 -*-


import requests
import json


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

    response = requests.post('http://${host_part_1}-api.${host_part_2}.com/user/login', headers=headers, data=data, verify=False)

    if response.status_code == 200:
        try:
            j = json.loads(response.content)
            return j['data']['token']
        except IOError:
            print('json parse error')
            return None
    else:
        print(response.status_code)
        return None


if __name__ == '__main__':
    print (login('${username}', '${password}'))
