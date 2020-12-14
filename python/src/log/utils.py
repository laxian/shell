# coding=utf-8

import zipfile

import os
import re
import requests
import platform


def get_name(url):
    index = url.rfind('/')
    return url[index + 1:]


def download(url, name=None):
    print("downloading...")
    r = requests.get(url, allow_redirects=True)
    if not name:
        name = get_name(url)
    with open(name, "wb") as code:
        code.write(r.content)


def unzip_2(zip_file, output):
    """
    TODO: 当前实现方式，可能有平台差异
    """
    os.system('unzip %s -d %s' % (zip_file, output))


def unzip(file, unzip_dir="."):
    """
    https://github.com/gzgdouru/pyutils/blob/ff17b6e75d18673bd43fc31fe8bc0888ffbe1676/compress.py
    """
    try:
        with zipfile.ZipFile(file) as zip_file:
            [zip_file.extract(name, unzip_dir) for name in zip_file.namelist()]
    except Exception as e:
        print('from %s to %s ' % (file, unzip_dir))
        raise RuntimeError("解压.zip文件出错, 原因:%r" % e)


def open_with_app(app, path):
    result = os.system("%s %s" % (app, path))
    if result != 0:
        name = platform.system()
        print(name)
        app=None
        if name == 'Windows':
            print('Windows系统')
            app='start'
        elif name == 'Linux':
            print('Linux系统')
            app='nautilus'
        elif name == 'Darwin':
            print('Mac OS')
            app='open'
        if app:
            if os.system('%s %s' % (app, path)) != 0:
                cannot_open(path)
        else:
            print('未知系统')
            cannot_open(path)
        
        
def cannot_open(path):
    print('已解压到：%s\n未配置正确的打开方式，请自行打开：' % path)


def get_time_part(url, re_str):
    return re.findall(re_str, url)[0]
