import json
import os
import sys


import requests
from src.log.api_login import login_and_save_token, check_response, clear_token
from src.log.config import Config
from src.log.token_exception import TokenException


def raw_status(robot_id, token=None):
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'authToken': token,
    'Origin': 'http://${host_part_nc}.${host_l}',
    'Referer': 'http://${host_part_nc}.${host_l}/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('page', '1'),
        ('pageSize', '10000'),
        ('robotId', robot_id),
        ('onlineStatus', ''),
        ('environment', ''),
        ('robotSystemVersion', ''),
        ('navAppVersion', ''),
    )

    url = 'http://${host_part_nc}-api.${host_l}/robot/information'
    print('=== === === 开始导航状态查询 === === ===')
    print(url)
    print(params)
    response = requests.get(url, headers=headers, params=params, verify=False)
    # print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def status_with_retry(robot_id):
    token = login_and_save_token()
    response = raw_status(robot_id, token)
    try:
        j = check_response(response)
        if 'data' in j:
            if 'list' in j['data']:
                lists = j['data']['list']
                if lists:
                    for m in lists:
                        pretty_print(m)
                    return lists
                else:
                    print('list empty')
            else:
                print('list not found')
                print(j)
        else:
            print('data not found')
    except TokenException as ex:
        clear_token()
        return status_with_retry(robot_id)
    except Exception as ex:
        print(type(ex))
        print(j)


def pretty_print(status_model):
    try:
        activeTime = status_model['activeTime'] if 'activeTime' in status_model else ''
        building = status_model['buildingInfo'] if 'buildingInfo' in status_model else ''
        env = status_model['environment'] if 'environment' in status_model else ''
        errorCodeConfigId = status_model['errorCodeConfigId'] if 'errorCodeConfigId' in status_model else ''
        navAppVersion = status_model['navAppVersion'] if 'navAppVersion' in status_model else ''
        offlineTime = status_model['offlineTime'] if 'offlineTime' in status_model else ''
        onlineStatus = status_model['onlineStatus'] if 'onlineStatus' in status_model else ''
        robotId = status_model['robotId'] if 'robotId' in status_model else ''
        robotSystemVersion = status_model['robotSystemVersion'] if 'robotSystemVersion' in status_model else ''
        settings = status_model['settings'] if 'settings' in status_model else ''
        ttsConfigId = status_model['ttsConfigId'] if 'ttsConfigId' in status_model else ''
        print('''
        ID：\t\t%s
        状态：\t\t%s
        系统：\t\t%s
        环境：\t\t%s
        navAppId: \t%s
        楼座：\t\t%s
        errcodeId: \t%s
        ttsId：\t\t%s
        在线时间：\t%s
        离线时间：\t%s
        设置：\n%s
        ''' % (robotId, onlineStatus, robotSystemVersion, env, navAppVersion, 
        building, errorCodeConfigId, ttsConfigId, activeTime, offlineTime, 
        json.dumps(json.loads(settings), sort_keys=True, indent=4, ensure_ascii=False)))

    except Exception as ex:
        print(status_model)
        print(ex)


if __name__ == '__main__':
    status_with_retry(sys.argv[1])