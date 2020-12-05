#!/usr/bin/env python

import requests
import time
import sys



def upload(robot_id, path, token, env='release'):
    timestamp = time.time() * 1000
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'authToken': token,
        'Origin': 'http://${host_part_1}.${host_part_2}.com',
        'Referer': 'http://${host_part_1}.${host_part_2}.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = '{"robotId":"%s","environment":"%s","logPath":"%s","startTime":1590984000000,"endTime":%d}' % (
        robot_id, env, path, timestamp)

    response = requests.post('http://${host_part_1}-api.${host_part_2}.com/robot/log/toUploadLog',
                             headers=headers, data=data, verify=False)
    if response.status_code == 200:
        print(response.content)
        return response.content
    else:
        print(response.status_code)
        return None


if __name__ == '__main__':
    robot_id = sys.argv[1]
    path = sys.argv[2]
    env = 'release' if len(sys.argv) <= 3 else sys.argv[3]
    print (upload(robot_id, path, '${token}', env))
