# coding=utf-8

import zipfile

import os
import re
import requests


def get_name(url):
    index = url.rfind('/')
    return url[index + 1:]


def download(url, name=None):
    print("downloading...")
    r = requests.get(url)
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
        raise RuntimeError(f"解压.zip文件出错, 原因:{e}")


def open_with_app(app, path):
    return os.system("%s %s" % (app, path))


def get_time_part(url, re_str):
    return re.findall(re_str, url)[0]
