# -*- coding: UTF-8 -*-

import os
import requests


def adb_auth():
    if not need_auth():
        return
    WEB_URL = "http://${adb_ip}:8080/scooter_adb/adb_get?hashCode="
    val = os.popen('adb reboot A55A')
    # hashcode = '65c6b596f7d33492d1c23179ae217927541d1bb7\n'
    print(hashcode)
    if not hashcode:
        print('未连接')
    elif hashcode == 0:
        print('没有拿到车上的hashCode,检查一下车与电脑的连接')
    elif 'AUTH already' in hashcode:
        print('已经解密')
    else:
        print('request hashCode %s' % hashcode)
        response = requests.get("%s%s" % (WEB_URL, hashcode))
        if response.status_code == 200:
            content = response.content.decode('utf-8')
        else:
            print(response.status_code)
            return
        new_hash_key = '5AA5%s' % content
        print(content)
        # print('adb reboot %s' % new_hash_key)
        val = os.popen('adb reboot %s' % new_hash_key)
        print(val.readline())


def need_auth():
    val = os.popen('adb shell uname')
    result = val.readline()
    if 'close' in result:
        return True
    return False


if __name__ == '__main__':
    adb_auth()