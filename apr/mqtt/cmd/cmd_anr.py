#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python cmd_client.py

import paho.mqtt.client as mqtt
import ssl
import uuid
from cmd_message import CmdMessage  # 导入 CmdMessage 类
from cmd_inner_message import CmdMessageInner  # 导入 CmdMessageInner 类
from rsa import (
    rsa_sign_sha1,
    load_private_key_from_file,
    load_public_key_from_file,
)  # 导入 CmdMessageInner 类

from dec import decryption
from aes2 import aes_decrypt_java, aes_encrypt_java
import os
import sys
import json
import base64
import time
# import subprocess
from get_pose_command import cmds


sys.path.append(".")

import io
# 实时刷新缓冲区
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, line_buffering=True)
# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取当前脚本目录的上层目录
parent_directory = os.path.dirname(script_directory)
# 将当前工作目录更改为当前脚本所在的路径
os.chdir(script_directory)

pri_key_path = os.path.join(f"{script_directory}/private", "private.pem")
pub_key_path = os.path.join(f"{script_directory}/private", "public.pem")
pubkey = load_public_key_from_file(pub_key_path)
prikey = load_private_key_from_file(pri_key_path)

# MQTT参数
username = "${username}"
password = "${cipher}"  # Replace with your actual password
client_id = "zwx2"
broker_address = "${host}"
broker_port = 13080
sub_topic = "robot/{robotId}/log/cmd/send"
pub_topic = "robot/{robotId}/log/cmd/command"
robot_id = ""

# SSL证书和密钥文件
ca_file = f"{script_directory}/private/ca_crt"
client_cert = f"{script_directory}/private/client_crt"
client_key = f"{script_directory}/private/client_key"

aeskey = None

robots = ["S3RAM2211C0003"]
# robots = ["S3RAM2252C0020","S3RAM2320C0011","S3RAM2325C0117","S3RAM2320C0003","S3RAM2252C0028","S3RAM2236C0011","S3RAM2252C0007","S3RAM2225C0037","S3RAM2225C0060","S3RAM2212C0017","S3RAM2245C0085","S3RAM2252C0090","S3RAM2245C0032","S3RAM2252C0098"]
# command = "settings get secure robot_id"
# command = "cat data/data/com.segway.robotic.app/shared_prefs/sp_preferences.xml"
# command = """
# sed -i 's#<int name="preference_key_volume" value="[0-9]\{1,3\}" />#<int name="preference_key_volume" value="66" />#' data/data/com.segway.robotic.app/shared_prefs/sp_preferences.xml 
# """
command = """
sed -i 's#<int name="preference_key_volume" value="[0-9]\{1,3\}" />#<int name="preference_key_volume" value="66" />#' data/data/com.segway.robotic.app/shared_prefs/sp_preferences.xml && \
kill -9 $(busybox awk 'NR==1 {print $3}' sdcard/logs_folder/com.segway.robotic.app/$(ls -t sdcard/logs_folder/com.segway.robotic.app/|head -n1)) && \
sleep 3 && \
input tap 70 550;input tap 70 550;input tap 70 550;input tap 70 550;input tap 70 550;input tap 70 550;input tap 70 550 && \
input tap 650 450;input tap 650 450;input tap 650 450;input tap 650 450
"""

anr = 'head -n3 /data/logs/anr/`ls /data/logs/anr | head -n 1`'
# anr = 'ls data/logs/anr'
# anr = 'grep am_anr -rI /data/logs/logcks'
# du = 'cd /sdcard/logs_folder/ && du -h -d 1'

commands = [
    # "ls"
    # 'pm install -r -i com.segway.robotic.app /sdcard/823_d2_th.apk',
    # 'pm dump com.segway.robotic.app | grep version'
    '''if [ `ls /data/logs/anr` ];then
    for f in `ls /data/logs/anr`;do
    cat /data/logs/anr/$f | head -n10
    done
    else
    echo "no anr"
    fi
    '''
]
index = 0

default_pos =  "input tap 650 450;input tap 650 450;input tap 650 450;input tap 650 450"

# 连接回调
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅主题
    # client.subscribe(sub_topic)


def on_subscribe(client, userdata, mid, granted_qos):
    print(f"---------------- Subscribed {client} {userdata} {mid} {granted_qos} {sub_topic} ----------------")
    send_verify()


# 消息接收回调
def on_message(client, userdata, msg):
    global index, default_pos
    json_object = json.loads(msg.payload.decode("utf-8"))
    content = json_object["responce"]
    if json_object["commandType"] == "verified":
        print("---------------- VERIFIED ----------------")
        print(json_object["responce"])

        with open(pri_key_path, "rb") as f:
            private_key = f.read()
        global aeskey
        aeskey = decryption(
            json_object["responce"],
            private_key,
        )
        print(aeskey)
        send_message(client, commands[index])
        index += 1
    elif json_object["commandType"] == "doRSA":
        print("---------------- doRSA ack ----------------")
        content = json_object["responce"]
        # print(content)

    elif json_object["commandType"] == "execute":
        if content.startswith("start handle message"):
            print("---------------- execute ack ----------------")
            # raw = content.split("'")
            # aes = raw[5].strip()
            # print(f"AES: {aes}")
            # dec = aes_decrypt_java(aes, aeskey)
            # print(f"Decrypted: {dec}")
        else:
            print("---------------- execute ----------------")
            print(content)
            if 'anr' in content:
                print(f"Anr: {robot_id}")
                clean_and_unsubscribe()
                index = 0
                return
            elif index >= len(commands):
                clean_and_unsubscribe()
                index = 0
            else:
                # time.sleep(1)
                print(f'index is: {index}')
                send_message(client, commands[index])
                index += 1
            

    else:
        print(f"Received message: {json_object['commandType']}")


def clean_and_unsubscribe():
    global sub_topic
    print(f"---------------- UNSUB {sub_topic} ----------------")
    client.unsubscribe(sub_topic)
    global robot_id, pub_topic
    sub_topic = sub_topic.replace(robot_id, "{robotId}")
    pub_topic = pub_topic.replace(robot_id, "{robotId}")
    robot_id = None


def make_message(cmd):
    global aeskey
    inner = CmdMessageInner()
    inner.set_command(cmd)
    inner_str = json.dumps(inner.to_dict())
    print(inner_str)
    en_inner_str = aes_encrypt_java(inner_str, aeskey)
    print(f"Encrypted inner message: {en_inner_str}")
    print(en_inner_str)
    message_payload = CmdMessage(command_type="execute", cmd_message_inner=en_inner_str)
    return message_payload


def send_message(client, msg):
    message_payload = make_message(msg)
    payload = json.dumps(message_payload.to_dict())
    print(f"================================ SEND {robot_id} ===================================")
    print(payload)
    print("============================== SEND END =================================")
    client.publish(pub_topic, payload=payload, qos=1)


def send_verify():
    # 发布消息
    # message_payload = '{"commandId":1,"commandType":"doRSA","mCmdMessageInner":"pwd"}'
    print(f"send message {pub_topic}")
    message_payload = CmdMessage(command_type="doRSA")
    hash = str(uuid.uuid4())
    # hash = '4558ac1466f54c13'
    inner = CmdMessageInner()
    inner.set_un_signed_string(hash)
    # print(base64.b64encode(rsa_sign_sha1(private_key=prikey, data=hash)).decode("utf-8"))
    inner.set_signed_string(
        base64.b64encode(rsa_sign_sha1(private_key=prikey, data=hash)).decode("utf-8")
    )
    message_payload.set_cmd_message_inner(json.dumps(inner.to_dict()))
    payload = json.dumps(message_payload.to_dict())
    client.publish(pub_topic, payload=json.dumps(message_payload.to_dict()), qos=1)


def close_connection():
    if client is None:
        return
    client.unsubscribe(sub_topic)
    client.disconnect()
    client.loop_stop()


def subscribe_robot(robot_id):
    global sub_topic, pub_topic
    sub_topic = sub_topic.replace("{robotId}", robot_id)
    pub_topic = pub_topic.replace("{robotId}", robot_id)
    print(f"Subscribing to {sub_topic} {robot_id}")
    print(f"Publishing to {pub_topic}")
    client.subscribe(sub_topic)


def connect_to_broker():

    global client
    # 创建MQTT客户端
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.tls_set(
        ca_certs=ca_file,
        certfile=client_cert,
        keyfile=client_key,
        cert_reqs=ssl.CERT_NONE,
    )  # 设置不验证服务器证书
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    # 连接到Broker
    client.connect(broker_address, broker_port)

    # 循环处理消息
    client.loop_start()


def send_once(cmd):
    send_message(client, cmd)


if __name__ == "__main__":

    connect_to_broker()

    # 持续运行，等待消息
    try:
        for robot in robots:
            print('\n')
            print('\n')
            print('---> handle robot: ' + robot)
            robot_id = robot
            subscribe_robot(robot)
            cnt = 0
            while robot_id is not None:
                try:
                    time.sleep(1)
                    print(".")
                    # cnt += 1
                    # if cnt > 10:
                    #     clean_and_unsubscribe()
                    #     break
                except KeyboardInterrupt:
                    print(f"Interrupted by user, skipping...{robot_id}")
                    clean_and_unsubscribe()
                    break
        print(f"Finished!")
        while True:
            pass
    except KeyboardInterrupt:
        close_connection()
        print("Disconnected and stopped the loop.")
        print(aeskey)