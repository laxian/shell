# -*- coding: UTF-8 -*-

import flask
import os
import sys
import socket


PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
print(sys.path)
from src.log.utils import *
 

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
    

def server_path(path):
    if not os.path.exists(path):
        print('%s does not exist' % path)
        return
        # throw Exception('path not exists')
    print(path)
    os.system('pwd')
    ip = get_host_ip()
    app = flask.Flask(__name__, static_folder=path)
    print(ip)
    app.run(host=ip, port=5000)

 
if __name__ == "__main__":
    server_path(sys.argv[1])