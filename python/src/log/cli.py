# usr/bin/bash python
# -*- encoding: utf-8 -*-

import sys
import os
import json
import time

from src.log.adb_auth import adb_auth
from src.log.adb_ex import dump_ex_log, dump_s2_log, dump_sys_log, pull_log_from_dir
from src.log.api_login import login_and_save_token
from src.log.api_query import query_with_retry, query_model_with_retry
from src.log.ore.api_query import query_with_retry as query_with_retry_ore, query_model_with_retry as query_model_with_retry_ore
from src.log.api_status import status_with_retry
from src.log.api_upload import upload_with_retry
from src.log.config import Config
from src.log.dumpnavLogs import nav_log_gui
from src.log.schedule import fetch_and_open, schedule
from src.log.ore.schedule import schedule as schedule_ore
from src.log.api_login_new import new_restore, new_available, new_status, robot_list
from src.log.utils import download, get_host_ip
from src.log.S1.api_s1_cn import s1_list


def segway_login(args=None):
    """
    登录并获取token，token会自动写入config
    """
    config = Config("config.json").config
    if not args:
        args = sys.argv[1:]
    if len(args) == 2:
        username = args[0]
        password = args[1]
    else:
        username = config["username"]
        password = config["password"]
    token = login_and_save_token()
    if token:
        if not config:
            config = Config("config.json").config
        config["username"] = username
        config["password"] = password
        config["token"] = token
        Config.dump(config)
        print(token)


def segway_config(args=None):
    keys = [
        "env",
        "open_app",
        "retry_limit",
        "retry_interval",
        "log_dir",
        "username",
        "password",
        "token",
        "log_start_time",
        "token2",
    ]
    hit = False
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        config = Config("config.json").config
        for arg in args:
            k, v = arg.split("=")
            if k in keys:
                hit = True
                config[k] = v
        if hit:
            Config.dump(config)


def segway_showconfig():
    config = Config("config.json").config
    print(json.dumps(config, sort_keys=True, indent=4, ensure_ascii=False))


def segway_upload(args=None):
    if len(sys.argv) > 2:
        robot_id = sys.argv[1]
        path = sys.argv[2]
    else:
        return

    config = Config("config.json").config
    log_start_time_f = config["log_start_time"]
    tick = time.time()
    if not log_start_time_f:
        # 默认拉取24小时日志
        print("拉取24小时日志")
        log_start_time = tick - 24 * 60 * 60
    else:
        print("拉取日志起始点：%s" % log_start_time_f)
        log_start_time = int(
            time.mktime(time.strptime(log_start_time_f, "%Y-%m-%d_%H:%M:%S")) * 1000
        )

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
        print("Usage: segway_query <robot_id> [index]")
        return
    result = query_with_retry(robot_id, index)
    if result:
        for u in result:
            print(u)
    else:
        print("没有查询到url")


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
        "startTime",
    ]
    if len(sys.argv) > 1:
        robot_id = sys.argv[1]
    else:
        print(
            """Usage: segway_query2 <robot_id> [option]
        option: 
        %s
        Samples:
        查询logPath=/sdcard/ex的日志，打印logPath和logUrl
        segway_query2 <id> logPath=/sdcard/ex logUrl
        """
            % all_keys
        )
        return
    result = query_model_with_retry(robot_id)
    if len(sys.argv) == 2:
        if result:
            for u in result:
                print(json.dumps(u, sort_keys=True, indent=4, ensure_ascii=False))
        else:
            print("没有查询到url")
    else:
        args = []
        for arg in sys.argv[2:]:
            if "=" in arg:
                k, v = arg.split("=")
                result = [
                    item for item in result if k in item.keys() and v == item.get(k)
                ]
                args.append(k)
            else:
                args.append(arg)
        for u in result:
            # 对每一个model遍历输入的keys，如有一命中，即为命中
            hit = False
            print("---------")
            for k in args:
                if k in all_keys and k in u:
                    hit = True
                    break
            # 不含key的，不显示
            if not hit:
                continue
            for k in args:
                if k in u:
                    print(
                        json.dumps(u[k], sort_keys=True, indent=4, ensure_ascii=False)
                    )
                    

def segway_query_ore():
    if len(sys.argv) == 3:
        robot_id = sys.argv[1]
        index = int(sys.argv[2])
    elif len(sys.argv) == 2:
        robot_id = sys.argv[1]
        index = -1
    else:
        print("Usage: segway_query_ore <robot_id> [index]")
        return
    result = query_with_retry_ore(robot_id, index)
    if result:
        for u in result:
            print(u)
    else:
        print("没有查询到url")


def segway_query2_ore():
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
        "startTime",
    ]
    if len(sys.argv) > 1:
        robot_id = sys.argv[1]
    else:
        print(
            """Usage: segway_query2_ore <robot_id> [option]
        option: 
        %s
        Samples:
        查询logPath=/sdcard/ex的日志，打印logPath和logUrl
        segway_query2_ore <id> logPath=/sdcard/ex logUrl
        """
            % all_keys
        )
        return
    result = query_model_with_retry_ore(robot_id)
    if len(sys.argv) == 2:
        if result:
            for u in result:
                print(json.dumps(u, sort_keys=True, indent=4, ensure_ascii=False))
        else:
            print("没有查询到url")
    else:
        args = []
        for arg in sys.argv[2:]:
            if "=" in arg:
                k, v = arg.split("=")
                result = [
                    item for item in result if k in item.keys() and v == item.get(k)
                ]
                args.append(k)
            else:
                args.append(arg)
        for u in result:
            # 对每一个model遍历输入的keys，如有一命中，即为命中
            hit = False
            print("---------")
            for k in args:
                if k in all_keys and k in u:
                    hit = True
                    break
            # 不含key的，不显示
            if not hit:
                continue
            for k in args:
                if k in u:
                    print(
                        json.dumps(u[k], sort_keys=True, indent=4, ensure_ascii=False)
                    )


def segway_auto(args=None):
    if len(sys.argv) < 3:
        print(
            """
        上传查询下载打开日志
        Usage: segway_auto <robot_id> <path>
        """
        )
        return
    elif len(sys.argv) == 3:
        schedule(sys.argv[1], sys.argv[2])
    else:
        schedule(sys.argv[1], sys.argv[2], sys.argv[3])


def segway_nav(args=None):
    nav_log_gui()


def segway_adb(args=None):
    adb_auth()


def segway_download(args=None):
    if len(sys.argv) == 1:
        print("Usage: %s %s" % ("segway_download", "<url>"))
        return
    url = sys.argv[1]
    download(url)


def segway_fetch(args=None):
    if len(sys.argv) == 1:
        print("Usage: %s %s" % ("segway_fetch", "<url>"))
        return
    url = sys.argv[1]
    config = Config("config.json").config
    fetch_and_open(url, config["open_app"], config["log_dir"])


def segway_pull_ex(args=None):
    dump_ex_log()


def segway_pull_s2(args=None):
    dump_s2_log()


def segway_pull_sys(args=None):
    dump_sys_log()


def segway_pull(args=None):
    if len(sys.argv) == 1:
        print("segway_pull <path>")
    else:
        pull_log_from_dir(sys.argv[1])


def segway_status(args=None):
    if len(sys.argv) == 1:
        print("segway_status <robot_id>")
    else:
        status_with_retry(sys.argv[1])


def segway_restore(args=None):
    if len(sys.argv) == 1:
        print("segway_restore <robot_id> [dev|alpha|internal|release=" "]")
    elif len(sys.argv) == 2:
        new_restore(sys.argv[1])
    else:
        new_restore(sys.argv[1], env=sys.argv[2])


def segway_available(args=None):
    if len(sys.argv) == 1:
        print(
            "segway_available <robot_id> [true|false] [dev|alpha|internal|release=" "]"
        )
    elif len(sys.argv) == 2:
        new_available(sys.argv[1], "true")
    elif len(sys.argv) == 3:
        new_available(sys.argv[1], sys.argv[2])
    else:
        new_available(sys.argv[1], sys.argv[2], env=sys.argv[3])


def segway_robots(args=None):
    """新业务后台机器人列表"""
    if len(sys.argv) == 1:
        robots = robot_list()
        print(robots)
    elif len(sys.argv) == 2:
        robots = robot_list(env=sys.argv[1])
        print("================================")
        print(robots)


def segway_status2(args=None):
    """新业务后台机器人实时RM"""
    if len(sys.argv) == 1:
        new_status()
    elif len(sys.argv) == 2:
        new_status(sys.argv[1])
    else:
        new_status(sys.argv[1], env=sys.argv[2])


def segway_s1(args=None):
    """S1新业务后台机器人实时状态"""
    if len(sys.argv) == 1:
        s1_list()
    elif len(sys.argv) >= 2:
        s1_list(env=sys.argv[1])


def segway_ore(args=None):
    if len(sys.argv) < 3:
        print(
            """
        上传查询下载打开日志[ore环境]
        Usage: segway_auto <robot_id> <path>
        """
        )
        return
    elif len(sys.argv) == 3:
        schedule_ore(sys.argv[1], sys.argv[2])
    else:
        schedule_ore(sys.argv[1], sys.argv[2], sys.argv[3])


def segway_share(args=None):
    """
    开启本地文件服务器，分享文件或目录
    """
    if len(sys.argv) == 1:
        print(
            """Usage: %s %s
        开启简易文件服务器，在内网快速共享文件
        """
            % ("segway_share", "<path>")
        )
    else:
        path = sys.argv[1]
        ip = get_host_ip()
        port = 5000
        if os.path.isfile(path):
            name = os.path.basename(path)
            path = os.path.dirname(path)
            print("http://%s:%d/%s" % (ip, port, name))
        else:
            print("http://%s:%s" % (ip, port))
        if sys.version_info.major == 2:
            os.system("python -m SimpleHTTPServer 5000")
        else:
            os.system("python -m http.server 5000")


def usage(args=None):
    print(
        """author: ${username}
version 0.2.0
Commands:
    
    配置类：
    segway_config 个性化配置：可配置项见配置部分
    segway_showconfig 显示配置
    
    一键展现日志：
    segway_auto <robot_id> <log_path> <yyyy-mm-dd_HH:MM:SS|\d+(h|d|m)> (上传->查询->拉取->下载->打开)自动获取远程日志
        开始时间在配置中配置，如果没配置，则默认拉取24小时内的日志。否则：需要参数3.
        参数3可以使为空则为now；
        也可以指定'%Y-%m-%d_%H:%M:%S'格式的日志截止时间；
        也可以指定1d、2h、30m格式，分别对应1天、2小时、30分钟，暂不支持负数，在开始时间上加上此时间段为结束时间。
    segway_ore <robot_id> <log_path> <yyyy-mm-dd_HH:MM:SS|\d+(h|d|m)> (上传->查询->拉取->下载->打开)自动获取远程日志
        开始时间在配置中配置，如果没配置，则默认拉取24小时内的日志。否则：需要参数3.
        参数3可以使为空则为now；
        也可以指定'%Y-%m-%d_%H:%M:%S'格式的日志截止时间；
        也可以指定1d、2h、30m格式，分别对应1天、2小时、30分钟，暂不支持负数，在开始时间上加上此时间段为结束时间。
    
    分步拉日志：
    segway_login 手动登录刷新token，一般无需手动执行
    segway_upload <robot_id> 上传指定robot_id的日志
    segway_download <url> 下载日志
    segway_fetch <url>  下载并打开日志
    segway_query <robot_id> [index] 查询日志url
    segway_query2 <robot_id> [option] 高级查询，输入segway_query2 获取帮助
    segway_query_ore <robot_id> [index] 查询日志url
    segway_query2_ore <robot_id> [option] 高级查询，输入segway_query2_ore 获取帮助
    segway_status <robot_id> 格式化打印机器人状态（导航）
    
    新业务后台接口：
    segway_status2 [robot_id] [dev|alpha|...] 格式化打印机器人状态（业务）
    segway_restore <robot_id> [dev|alpha|...]重置，一键初始化机器人
    segway_available <robot_id> [false|true|] [dev|alpha|...]可用
    segway_robots [dev|alpha|...]可用
    
    新业务业务后台-S1-国内
    segway_s1 [dev|release='']餐厅机器人列表+实时状态
    
    本机工具：
    segway_adb adb 解密
    segway_share <file_path> 开启文件服务器，以url方式分享本地文件
    
    本地拉日志快捷命令：
    segway_nav GUI窗口，拉取nav日志 
    segway_pull <path> 本地拉取指定path日志并打开
    segway_pull_ex [Deprecated]本地拉取/sdcard/ex 日志并打开
    segway_pull_s2 本地拉取/sdcard/logs_folder/com.segway.robotic.app 日志并打开
    segway_pull_sys 本地拉取/data/logs 日志并打开
    """
    )


def segway(args=None):
    usage()
    return
