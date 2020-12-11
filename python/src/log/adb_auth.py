# -*- coding: UTF-8 -*-

import os
import requests


def adb_auth():
    WEB_URL = "http://${adb_ip}:8080/scooter_adb/adb_get?hashCode="
    val = os.popen('adb reboot A55A')
    hashcode = val.readline()
    print(hashcode)
    if not hashcode:
        print('未连接')
    elif hashcode == 0:
        print('没有拿到车上的hashCode,检查一下车与电脑的连接')
    elif hashcode == 'AUTH already':
        print('已经解密')
    else:
        print('request hashCode %s' % hashcode)
        response = requests.get("%s%s" % (WEB_URL, hashcode))
        if response.status_code == 200:
            content = response.content
        else:
            print(response.status_code)
        new_hash_key = '5AA5%s' % content
        print(content)
        val = os.popen('adb reboot %s' % new_hash_key)
        print(val.readline())


if __name__ == '__main__':
    adb_auth()