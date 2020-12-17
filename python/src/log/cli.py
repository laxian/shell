# usr/bin/bash python
# -*- encoding: utf-8 -*-

import sys
import json
import time

from src.log.adb_auth import adb_auth
from src.log.adb_ex import dump_ex_log, dump_sys_log, pull_log_from_dir
from src.log.api_login import login_and_save_token
from src.log.api_query import query_with_retry, query_model_with_retry
from src.log.api_status import get_status
from src.log.api_upload import upload_with_retry
from src.log.config import Config
from src.log.dumpnavLogs import nav_log_gui
from src.log.schedule import fetch_and_open, schedule
from src.log.api_login_old import api_restore, api_available, api_arrive
from src.log.utils import download


def segway_login(args=None):
    """
    登录并获取token，token会自动写入config
    """
    config = Config('config.json').config
    if not args:
        args = sys.argv[1:]
    if len(args) == 2:
        username = args[0]
        password = args[1]
    else:
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
    keys = ['env', 'open_app', 'retry_limit', 'retry_interval', 'log_dir', 'username', 'password', 'token', 'log_start_time']
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
    print(json.dumps(config, sort_keys=True, indent=4, ensure_ascii=False))


def segway_upload(args=None):
    if len(sys.argv) > 2:
        robot_id = sys.argv[1]
        path = sys.argv[2]
    else:
        return

    config = Config('config.json').config
    log_start_time_f = config['log_start_time']
    if not log_start_time_f:
        # 默认拉取24小时日志
        print('拉取24小时日志')
        log_start_time = tick - 24 * 60 * 60
    else:
        print('拉取日志起始点：%s' % log_start_time_f)
        log_start_time = int(time.mktime(time.strptime(log_start_time_f, '%Y-%m-%d_%H:%M:%S')) * 1000)

    result = upload_with_retry(robot_id, path, log_start_time, None, None)
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
    result = query_with_retry(robot_id, index)
    if result:
        for u in result:
            print(u)
    else:
        print('没有查询到url')


def segway_query2():
    all_keys = [
    "ackTime",
    "commandId",
    "commandMessage",
    "commandStatus",
    "createBy",
    "createTime",
    "endTime",
    "environment",
    "id",
    "logName",
    "logPath",
    "logType",
    "logUrl",
    "responseTime",
    "robotId",
    "startTime"
    ]
    if len(sys.argv) > 1:
        robot_id = sys.argv[1]
    else:
        print('''Usage: segway_query2 <robot_id> [option]
        option: 
        %s
        Samples:
        查询logPath=/sdcard/ex的日志，打印logPath和logUrl
        segway_query2 <id> logPath=/sdcard/ex logUrl
        ''' % all_keys)
        return
    result = query_model_with_retry(robot_id)
    if len(sys.argv) == 2:
        if result:
            for u in result:
                print(u)
        else:
            print('没有查询到url')
    else:
        args = []
        for arg in sys.argv[2:]:
            if '=' in arg:
                k,v = arg.split('=')
                result = [item for item in result if k in item.keys() and v == item.get(k)]
                args.append(k)
            else:
                args.append(arg)
        all_in = True
        for u in result:
            print('---------')
            for k in args:
                if k in all_keys and k not in u:
                    all_in = False
                    break
            # 不含key的，不显示
            if not all_in:
                break
            for k in args:
                print(json.dumps(u[k], sort_keys=True, indent=4, ensure_ascii=False))


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


def segway_nav(args=None):
    nav_log_gui()


def segway_adb(args=None):
    adb_auth()


def segway_download(args=None):
    if len(sys.argv) == 1:
        print("Usage: %s %s" % ('segway_download', '<url>'))
        return
    url = sys.argv[1]
    download(url)

def segway_fetch(args=None):
    if len(sys.argv) == 1:
        print("Usage: %s %s" % ('segway_fetch', '<url>'))
        return
    url = sys.argv[1]
    config = Config('config.json').config
    fetch_and_open(url, config['open_app'], config['log_dir'])

def segway_pull_ex(args=None):
    dump_ex_log()

def segway_pull_sys(args=None):
    dump_sys_log()

def segway_pull(args=None):
    if len(sys.argv) == 1:
        print('segway_pull <path>')
    else:
        pull_log_from_dir(sys.argv[1])

def segway_status(args=None):
    if len(sys.argv) == 1:
        print('segway_status <robot_id>')
    else:
        get_status(sys.argv[1])

def segway_restore(args=None):
    if len(sys.argv) == 1:
        print('segway_restore <robot_id>')
    elif len(sys.argv) == 2:
        api_restore(sys.argv[1])
    else:
        api_restore(sys.argv[1], sys.argv[2])

def segway_available(args=None):
    if len(sys.argv) == 1:
        print('segway_available <robot_id> [true|false] [dev|alpha|internal|release]')
    elif len(sys.argv) == 2:
        api_available(sys.argv[1], 'true')
    elif len(sys.argv) == 3:
        api_available(sys.argv[1], sys.argv[2])
    else:
        api_available(sys.argv[1], sys.argv[2], sys.argv[3])

def segway_arrive(args=None):
    if len(sys.argv) == 1:
        print('segway_arrive <robot_id>')
    elif len(sys.argv) == 2:
        api_arrive(sys.argv[1])
    else:
        api_arrive(sys.argv[1], sys.argv[2])

def usage(args=None):
    print("""Commands:
    segway_adb adb 解密
    segway_auto <robot_id> <log_path> (上传->查询->拉取->下载->打开)自动获取远程日志
    segway_config 个性化配置：可配置项见配置部分
    segway_download <url> 下载日志
    segway_fetch <url>  下载并打开日志
    segway_nav GUI窗口，拉取nav日志 
    segway_login 登录刷新token
    segway_pull <path> 本地拉取指定path日志并打开
    segway_pull_ex 本地拉取/sdcard/ex 日志并打开
    segway_pull_sys 本地拉取/data/logs 日志并打开
    segway_query <robot_id> [index] 查询日志url
    segway_query2 <robot_id> [option] 高级查询，输入segway_query2 获取帮助
    segway_showconfig 显示配置
    segway_upload <robot_id> 上传指定robot_id的日志
    segway_status <robot_id> 格式化打印机器人状态
    segway_restore <robot_id> 重置
    segway_available <robot_id> 可用
    segway_arrive <robot_id> 到达
    """)

def segway(args=None):
    usage()
    return


