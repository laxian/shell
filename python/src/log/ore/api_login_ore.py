#!/usr/bin/env python

# -*- coding: UTF-8 -*-


import json

import requests

from src.log.token_exception import TokenException
from src.log.config import Config


def raw_login(username, password):
    """
    登录海外oregon，返回json
    :param username:
    :param password:
    :return:
    """
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://navcenter-oregon.${host_l}',
        'Referer': 'http://navcenter-oregon.${host_l}/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"username":"%s","password":"%s"}' % (username, password)
    url = 'https://usercenter-oregon.${host_l}/usercenter/user/login'
    print('=== === === 开始登陆 === === ===')
    print(url)
    print(data)

    response = requests.post(url, headers=headers, data=data, verify=False)

    print(response)
    print(response.content.decode('utf-8'))
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def get_token(response):
    j = json.loads(response)
    print(j)
    code = j['resultCode']
    if code == 9000:
        return j['data']['token']
    else:
        print(j['resultDesc'])


def login_and_save_token():
    config = Config('config.json').config
    if 'token_ore' not in config or not config['token_ore']:
        if not config['username'] or not config['password']:
            print('请先配置账号密码')
            return
        else:
            response = raw_login(config['username'], config['password'])
            token = get_token(response)
            if token:
                config['token_ore'] = token
                Config.dump(config)
                return token
            else:
                print('登录失败')
    else:
        print('已有token: %s' % config['token_ore'])
        return config['token_ore']

def check_response(response):
    j = json.loads(response)
    code = j['resultCode']
    if code == 9006 or code == 4006:
        raise TokenException(j['resultDesc'])
    else:
        return j

def clear_token():
    config = Config('config.json').config
    config['token_ore'] = None
    Config.dump(config)



if __name__ == '__main__':
    # print(login_and_save_token())
    print(raw_login('${username}', '${password}'))
