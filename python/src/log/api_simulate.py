import requests
import json
from src.log.config import Config
from src.log.token_exception import TokenException
from src.log.api_login_old import *


def api_broken(robotId, env='dev', errorCode=110123, msg='test'):
    '''
    test api, no token verify
    '''
    params = (
        ('robotId', robotId),
        ('code', errorCode),
        ('msg', msg),
    )

    response = requests.get(
        'https://api-gate-%s-delivery.${host_part_2}.com/test/robot/simulation/error' % env, params=params)

    print(response.content.decode('utf-8'))


def task_list(token, env='dev'):
    env = env+'-' if env else ''
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
        ('pageSize', '10000'),
    )

    response = requests.get(
        'https://api-gate-%sdelivery.${host_part_2}.com/web/transport/task/info/list' % env, headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def task_list_parser(j, robotId=None):
    if not j:
        return None
    size = j['data']['totalSize']
    tasks = j['data']['list']
    return [l['taskId'] for l in tasks if robotId in l.values() ] if robotId else [ l['taskId'] for l in tasks ]
    if size == 0:
        return []
    


def get_all_tasks(robotId=None, env='dev'):
    token = login_and_save_token(env)
    content = task_list(token, env)
    try:
        j = check_response(content)
        tasks = task_list_parser(j, robotId)
        return tasks
    except TokenException as ex:
        clear_token()
        get_all_tasks(robotId, env)
    except Exception as ex:
        print(j)
        print(ex)

def raw_interrupt_tasks(token, tasks, env='dev'):
    env = env+'-' if env else ''
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'token': token,
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://%sdelivery.${host_part_2}.com' % env,
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://%sdelivery.${host_part_2}.com/' % env,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # data = '{"taskIds":["37632ae8bca041b3989e4e8f1e618ba2"]}'
    data = json.dumps({"taskIds": tasks})
    print(data)

    response = requests.post('https://api-gate-%sdelivery.${host_part_2}.com/web/transport/task/interrupt' % env, headers=headers, data=data)
    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def interrupt_tasks(tasks, env='dev'):
    token = login_and_save_token(env)
    content = raw_interrupt_tasks(token, tasks, env)
    print(content)
    try:
        j = check_response(content)
        print('------------------------')
    except TokenException as ex:
        clear_token()
        interrupt_tasks(env, robotId)
    except Exception as ex:
        print(j)
        print(ex)


def raw_complete(token, taskId, env):
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

    data = '{"taskId":"%s"}' % taskId

    url = 'https://api-gate-%sdelivery.${host_part_2}.com/web/transport/task/accomplish' % env
    print(url)
    print(data)
    response = requests.post(url, headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def task_complete(taskId=None, env='dev'):
    token = login_and_save_token(env)
    content = raw_complete(token, taskId, env)
    try:
        j = check_response(content)
        print(j)
    except TokenException as ex:
        clear_token()
        task_complete(taskId, env)
    except Exception as ex:
        print(j)
        print(ex)


def raw_shield_nav(token, robotId, shield='true', env='dev'):
    env = env+'-' if env else ''

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

    data = json.dumps({"robotId":robotId,"shieldNav":shield})

    url = 'https://api-gate-%sdelivery.${host_part_2}.com/web/transport/robot/config/shieldNav' % env
    print(url)
    print(data)
    response = requests.post(url, headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)

def shield_nav(robotId, shield='true', env='dev'):
    token = login_and_save_token(env)
    content = raw_shield_nav(token, robotId, shield, env)
    try:
        j = check_response(content)
        print(j)
    except TokenException as ex:
        clear_token()
        shield_nav(env, shield, taskId)
    except Exception as ex:
        print(j)
        print(ex)

def clear_tasks(robotId, env='dev'):
    ids = get_all_tasks('EVT8-10')
    print(ids)
    interrupt_tasks(ids)
    for task in ids:
        task_complete(task)


if __name__ == '__main__':
    print('----------------------------------------------------------------')
    ids = get_all_tasks('EVT8-10')
    print(ids)
    interrupt_tasks(ids)
    for task in ids:
        task_complete(task)
    # shield_nav('EVT8-10', 'false')