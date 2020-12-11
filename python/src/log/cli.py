# usr/bin/bash python
# -*- encoding: utf-8 -*-

import sys

from src.log.adb_auth import adb_auth
from src.log.api_login import login, login_and_save_token
from src.log.api_query import query_with_retry, query_with_retry2
from src.log.api_upload import upload_with_retry
from src.log.config import Config
from src.log.schedule import schedule
from src.log.dumpnavLogs import local_log


def segway_login(args=None):
    if not args:
        args = sys.argv[1:]
    if len(args) == 2:
        username = args[0]
        password = args[1]
    else:
        config = Config('config.json').config
        username = config['username']
        password = config['password']
    token = login_and_save_token(username, password)
    if token:
        if not config:
            config = Config('config.json').config
        config['username'] = username
        config['password'] = password
        config['token'] = token
        Config.dump(config)
        print(token)


def segway_config(args=None):
    keys = ['env', 'open_app', 'retry_limit', 'retry_interval', 'log_dir', 'username', 'password', 'token']
    hit = False
    if len(sys.argv) > 1:
        args= sys.argv[1:]
        config = Config('config.json').config
        for arg in args:
            k, v = arg.split('=')
            if k in keys:
                hit = True
                config[k] = v
        if hit:
            Config.dump(config)


def segway_showconfig():
    config = Config('config.json').config
    print(config)


def segway_upload(args=None):
    if len(sys.argv) > 2:
        robot_id = sys.argv[1]
        path = sys.argv[2]
    result = upload_with_retry(robot_id, path, None, None)
    if result:
        print(result)


def segway_query():
    if len(sys.argv) == 3:
        robot_id = sys.argv[1]
        index = int(sys.argv[2])
    elif len(sys.argv) == 2:
        robot_id = sys.argv[1]
        index = -1
    else:
        print('Usage: segway_query <robot_id> [index]')
        return
    result = query_with_retry2(robot_id, index)
    for u in result:
        print(u)


def segway_auto(args=None):
    if len(sys.argv) < 3:
        print('''
        上传查询下载打开日志
        Usage: segway_auto <robot_id> <path>
        ''')
        return
    else:
        robot_id = sys.argv[1]
        path = sys.argv[2]
    schedule(robot_id, path)


def segway_local(args=None):
    local_log()


def segway_adb(args=None):
    adb_auth()
