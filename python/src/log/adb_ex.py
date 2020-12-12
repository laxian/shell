#!/usr/bin/env python

import os
import time

from src.log.config import Config



def dump_ex_log():
    pull_log_from_dir('/sdcard/ex')

def dump_sys_log():
    pull_log_from_dir('/data/logs')

def pull_log_from_dir(log_dir):
    print('----------------')
    config = Config('config.json').config
    parent = config['log_dir']
    device_id = get_device_id()
    dir = get_dir(parent)
    # 最终输出路径：日志父目录-设备id-格式化时间-设备日志目录
    final_dir = dir + log_dir.replace('/', '_')
    pull_log_to(from_dir=log_dir ,to_dir=final_dir)
    open_with_app(config['open_app'], final_dir)


def get_device_id():
    """
    get android device id
    """
    result = os.popen('adb devices | head -n 2 | tail -n 1').readline().strip()
    if result:
        print(result.split('\t')[0])
        return result.split('\t')[0]
    else:
        print('No devices found')

def get_time():
    tick = time.time()
    tf = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(tick))
    return tf

def get_dir(parent='.'):
    did = get_device_id()
    time_format = get_time()
    return os.path.join(parent,'%s_%s' % (did, time_format))

def pull_log_to(from_dir=None, to_dir=None):
    if not to_dir:
        dir = get_dir()
    if not from_dir:
        from_dir = '/sdcard/ex'
    result = os.popen('adb pull %s %s' % (from_dir, to_dir))
    print(result.read().strip())

def open_with_app(app='code', path='.'):
    return os.system("%s %s" % (app, path))



if __name__ == '__main__':
    # get_device_id()
    # pull_log_to()
    dump_sys_log()
