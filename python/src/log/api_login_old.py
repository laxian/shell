import requests

from src.log.config import Config
import json


def raw_login(username, password):
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://dev-delivery.${host_part_2}.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'http://dev-delivery.${host_part_2}.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"username":"%s","password":"%s"}' % (username, password)

    response = requests.post('https://api-gate-dev-delivery.${host_part_2}.com/web/user/login', headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_restore(token, robot_id):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://dev-delivery.${host_part_2}.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://dev-delivery.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"robotId":"%s"}' % robot_id

    response = requests.post('https://api-gate-dev-delivery.${host_part_2}.com/web/transport/robot/simulation/arrive', headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_arrive(token, robot_id):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://dev-delivery.${host_part_2}.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://dev-delivery.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"available":false,"robotIds":["%s"]}' % robot_id

    response = requests.post('https://api-gate-dev-delivery.${host_part_2}.com/web/transport/robot/config/available', headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_available(token, robot_id):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://dev-delivery.${host_part_2}.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://dev-delivery.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"robotId":"%s"}' % robot_id

    response = requests.post('https://api-gate-dev-delivery.${host_part_2}.com/web/transport/robot/restore', headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def get_token(response):
    j = json.loads(response)
    code = j['code']
    if code == 200:
        return j['data']['token']
    else:
        print(j['message'])
        

def login_and_save_token():
    config = Config('config.json').config
    if 'token2' not in config or not config['token2']:
        if not config['username'] or not config['password']:
            print('请先配置账号密码')
            return
        else:
            response = raw_login(config['username'], config['password'])
            token = get_token(response)
            if token:
                config['token2'] = token
                print(config)
                Config.dump(config)
                return token
            else:
                print('登录失败')
    else:
        print('已有token: %s' % config['token2'])
        return config['token2']

def check_response(response):
    j = json.loads(response)
    code = j['code']
    if code == 4006:
        raise TokenException(j['message'])
    else:
        return j


def api_restore(robot_id):
    token = login_and_save_token()
    response = raw_restore(token, robot_id)
    try:
        print(check_response(response))
    except TokenException as ex:
        clear_token()
        api_restore(robot_id)

def api_available(robot_id):
    token = login_and_save_token()
    response = raw_restore(token, robot_id)
    try:
        print(check_response(response))
    except TokenException as ex:
        clear_token()
        api_available(robot_id)

def api_arrive(robot_id):
    token = login_and_save_token()
    response = raw_restore(token, robot_id)
    try:
        print(check_response(response))
    except TokenException as ex:
        clear_token()
        api_arrive(robot_id)

def clear_token():
    config = Config('config.json').config
    config['token'] = None
    Config.dump(config)


if __name__ == '__main__':
    # login_and_save_token()
    print(api_restore('EVT6-2-1'))
    print(api_available('EVT6-2-1'))
    print(api_arrive('EVT6-2-1'))