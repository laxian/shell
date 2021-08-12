import requests

import json
from src.log.config import Config
from src.log.token_exception import TokenException
from functools import wraps

def p(obj, *args, **kw):
    print(obj)

def relogin(h=p, **kw):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            token = login_and_save_token(kwargs['env']) if 'env' in kwargs else login_and_save_token()
            print('%s %s %s' % (token, args, kwargs))
            content = func(token, *args, **kwargs)
            try:
                j = check_response(content)
                return h(j, **kwargs)
            except TokenException as ex:
                clear_token()
                return wrapped_function(*args, **kwargs)
            except Exception as ex:
                print(ex)
            # return func(token, *args, **kwargs)
        return wrapped_function
    return logging_decorator

def raw_login(username, password, env):
    env = env + '-' if env else ''
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://%sdelivery.${host_part_2}.com' % env,
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'http://%sdelivery.${host_part_2}.com/' % env,
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"username":"%s","password":"%s"}' % (username, password)
    url = 'https://api-gate-%sdelivery.${host_part_2}.com/web/user/login' % env
    
    print('=== === === 开始登陆旧版业务后台 === === ===')

    print(url)
    print(data)
    response = requests.post(url, headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_restore(token, robot_id, env):
    env = env + '-' if env else ''
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://%sdelivery.${host_part_2}.com' % env,
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://%sdelivery.${host_part_2}.com/' % env,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"robotId":"%s"}' % robot_id

    response = requests.post('https://api-gate-%sdelivery.${host_part_2}.com/web/transport/robot/restore' % env, headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_arrive(token, robot_id, env):
    env = env + '-' if env else ''
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://%sdelivery.${host_part_2}.com' % env,
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://%sdelivery.${host_part_2}.com/' % env,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"robotId":"%s"}' % robot_id

    url = 'https://api-gate-%sdelivery.${host_part_2}.com/web/transport/robot/simulation/arrive' % env
    print(url)
    print(data)
    response = requests.post(url, headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_status(token, robot_id, env):
    env = env + '-' if env else ''
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Origin': 'http://%sdelivery.${host_part_2}.com' % env,
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://%sdelivery.${host_part_2}.com/' % env,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('pageNo', '1'),
        ('pageSize', '10'),
        ('robotId', '%s' % robot_id),
    )

    url = 'https://api-gate-%sdelivery.${host_part_2}.com/web/transport/robot/info/list' % env
    response = requests.get(url, headers=headers, params=params)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def raw_available(token, robot_id, available, env):
    env = env + '-' if env else ''
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://%sdelivery.${host_part_2}.com' % env,
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://%sdelivery.${host_part_2}.com/' % env,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"available":%s,"robotIds":["%s"]}' % (available, robot_id)
    url='https://api-gate-%sdelivery.${host_part_2}.com/web/transport/robot/config/available' % env
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def get_token(response):
    j = json.loads(response)
    print(j)
    code = j['code']
    if code == 200:
        return j['data']['token']
    else:
        print(j['message'])
        

def login_and_save_token(env='dev'):
    config = Config('config.json').config
    if 'token2' not in config or not config['token2']:
        if not config['username'] or not config['password']:
            print('请先配置账号密码')
            return
        else:
            response = raw_login(config['username'], config['password'], env)
            token = get_token(response)
            if token:
                config['token2'] = token
                # print(config)
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
    if code == 4006 or code == 4007:
        raise TokenException(j['message'])
    elif code != 200:
        raise Exception(j['message'])
    else:
        return j

@relogin()
def api_restore(token, robot_id, env='dev'):
    return raw_restore(token, robot_id, env)

@relogin()
def api_available(token, robot_id, available, env='dev'):
    return raw_available(token, robot_id, available, env)

@relogin()
def api_arrive(token, robot_id, env='dev'):
    return raw_arrive(token, robot_id, env)

def api_status(robot_id, env='dev'):
    token = login_and_save_token(env)
    response = raw_status(token, robot_id, env)
    try:
        # print(json.dumps(check_response(response), sort_keys=True, indent=4, ensure_ascii=False))
        response_model = check_response(response)
        lists = response_model['data']['list']
        if lists:
            for u in lists:
                pretty_print(u)
        else:
            print(response_model)
    except TokenException as ex:
        clear_token()
        api_status(robot_id, env)
    except Exception as ex:
        print(type(ex))
        print(response_model)

def pretty_print(status_model):
    try:
        robotId = status_model['robotId'] if 'robotId' in status_model else ''
        robotStatus = status_model['robotStatus'] if 'robotStatus' in status_model else ''
        available = status_model['available'] if 'available' in status_model else ''
        online = status_model['online'] if 'online' in status_model else ''
        broken = status_model['broken'] if 'broken' in status_model else ''
        battery = status_model['battery'] if 'battery' in status_model else ''
        nickname = status_model['nickname'] if 'nickname' in status_model else ''
        boxSize = status_model['boxSize'] if 'boxSize' in status_model else ''
        preemptBoxSize = status_model['preemptBoxSize'] if 'preemptBoxSize' in status_model else ''
        remanentBoxSize = status_model['remanentBoxSize'] if 'remanentBoxSize' in status_model else ''
        usingBoxSize = status_model['usingBoxSize'] if 'usingBoxSize' in status_model else ''
        home = status_model['home'] if 'home' in status_model else ''
        buildingName = status_model['buildingName'] if 'buildingName' in status_model else ''
        stationName = status_model['stationName'] if 'stationName' in status_model else ''
        subarea = status_model['subarea'] if 'subarea' in status_model else ''
        warn = status_model['warn'] if 'warn' in status_model else ''
        print('''---------------------------------------
        ID:\t\t%s
        状态:\t\t%s
        可用:\t\t%s
        在线:\t\t%s
        broken:\t\t%s
        电量:\t\t%s
        昵称:\t\t%s
        箱格数:\t\t%s
        预占:\t\t%s
        剩余:\t\t%s
        已使用:\t\t%s
        待命点:\t\t%s
        当前站点:\t%s
        楼宇:\t\t%s
        楼座:\t\t%s
        警告:\t\t%s
        ''' % (robotId, robotStatus, available, online, broken, battery, nickname, boxSize, 
        preemptBoxSize, remanentBoxSize, usingBoxSize, home, stationName, buildingName, subarea, warn))
    except expression as identifier:
        print(json.dumps(status_model, sort_keys=True, indent=4, ensure_ascii=False))

def clear_token():
    config = Config('config.json').config
    config['token2'] = None
    Config.dump(config)


if __name__ == '__main__':
    # login_and_save_token()
    # print(api_restore('EVT6-2-1'))
    # print(api_available('EVT6-2-1'))
    # print(api_arrive('EVT6-2-1'))
    print(api_status('EVT6-2-1'))
    p('hello', robotId='EVT6-2-2')