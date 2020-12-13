import json
import requests
import sys
from src.log.config import Config
from src.log.api_login import login_and_save_token


def robot_status_api(robot_id, token=None):
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'authToken': token,
    'Origin': 'http://${host_part_1}.${host_part_2}.com',
    'Referer': 'http://${host_part_1}.${host_part_2}.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('page', '1'),
        ('pageSize', '10'),
        ('robotId', robot_id),
        ('onlineStatus', ''),
        ('environment', ''),
        ('robotSystemVersion', ''),
        ('navAppVersion', ''),
    )

    response = requests.get('http://${host_part_1}-api.${host_part_2}.com/robot/information', headers=headers, params=params, verify=False)
    print(response)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(response.status_code)


def get_status_data(robot_id, token=None):
    if not token:
        config = Config('config.json').config
        token = config['token']
    response = robot_status_api(robot_id, token)
    if response:
        j = json.loads(response)
        code = j['resultCode']
        if code == 9000:
            if 'data' in j:
                if 'list' in j['data']:
                    lists = j['data']['list']
                    if lists:
                        return lists[0]
                    else:
                        print('list empty')
                else:
                    print('list not found')
                    print(j)
            else:
                print('data not found')
        elif code == 9006:
            print(j['resultDesc'])
            raise RuntimeError(j['resultDesc'])
        else:
            print(j.get('resultDesc'))
    else:
        print('request failed')


def get_status_data_with_retry(robot_id, token=None):
    try:
        return get_status_data(robot_id, token)
    except RuntimeError as er:
        config = Config('config.json').config
        token = login_and_save_token(config['username'], config['password'])
        if token:
            return get_status_data(robot_id, token)


def pretty_print(status_model):
    try:
        activeTime = status_model['activeTime']
        building = status_model['buildingInfo']
        env = status_model['environment']
        errorCodeConfigId = status_model['errorCodeConfigId']
        navAppVersion = status_model['navAppVersion']
        offlineTime = status_model['offlineTime']
        onlineStatus = status_model['onlineStatus']
        robotId = status_model['robotId']
        robotSystemVersion = status_model['robotSystemVersion']
        settings = status_model['settings']
        ttsConfigId = status_model['ttsConfigId']
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


def get_status(robot_id):
    result = get_status_data_with_retry(robot_id)
    pretty_print(result)


if __name__ == '__main__':
    get_status(sys.argv[1])