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


def unzip(file, output):
    os.system('unzip %s -d %s' % (file, output))


def open_with_app(app, path):
    return os.system("%s %s" % (app, path))


def get_time_part(url, re_str):
    return re.findall(re_str, url)[0]
