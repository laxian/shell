# usr/bin/bash python
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
    username = args[0]
    password = args[1]
    token = login_and_save_token(username, password)
    if token:
        config = Config('config.json').config
        config['username'] = username
        config['password'] = password
        config['token'] = token
        Config.dump(config)
        print(token)


def segway_config(env='release', open_app='code', retry_limit=20, retry_interval=1, log_dir='Users/admin/Downloads'):
    if len(sys.argv) == 6:
        env = sys.argv[1]
        open_app = sys.argv[2]
        retry_limit = sys.argv[3]
        retry_interval = sys.argv[4]
        log_dir = sys.argv[5]
    else:
        print("""
            segway_config env open_app retry_limit retry_interval log_dir
            """)
    config = Config('config.json').config
    config['env'] = env
    config['open_app'] = open_app
    config['retry_limit'] = retry_limit
    config['retry_interval'] = retry_interval
    config['log_dir'] = log_dir
    Config.dump(config)
    print(config)


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
