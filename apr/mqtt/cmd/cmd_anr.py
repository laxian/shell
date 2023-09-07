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

robots = ["S1RHM2110C0012","S1RHM2110C0014","S1RHM2110C0022","S1RHM2110C0023","S1RLM2048C0004","S1RLM2048C0005","S1RLM2048C0011","S1RLM2049C0005","S1RLM2052C0021","S1RLM2052C0043","S1RLM2053C0006","S1RLM2053C0007","S1RLM2053C0016","S1RLM2053C0017","S1RLM2103C0004","S1RLM2109C0011","S1RLM2109C0014","S1RLM2109C0022","S1RLM2109C0033","S1RLM2109C0040","S1RLM2111C0013","S1RLM2111C0020","S1RLM2111C0025","S1RLM2111C0030","S1RLM2111C0043","S1RLM2111C0051","S1RLM2111C0057","S1RLM2111C0061","S1RLM2112C0006","S1RLM2112C0007","S1RLM2113C0001","S1RLM2113C0019","S1RLM2113C0020","S1RLM2117C0001","S1RLM2119C0008","S1RLM2119C0009","S1RLM2120C0003","S1RLM2120C0014","S1RLM2120C0027","S1RLM2120C0031","S1RLM2120C0042","S1RLM2123C0028","S1RLM2123C0029","S1RLM2123C0036","S1RLM2123C0041","S1RLM2123C0054","S1RLM2124C0021","S1RLM2125C0002","S1RLM2129C0003","S1RLM2129C0005","S1RLM2129C0006","S1RLM2129C0011","S1RLM2129C0022","S1RLM2129C0049","S1RLM2138C0017","S1RLM2138C0023","S1RLM2138C0047","S1RLM2138C0048","S1RLM2138C0049","S1RLM2138C0056","S1RLM2138C0061","S1RLM2138C0064","S1RLM2139C0003","S1RLM2139C0004","S1RLM2139C0008","S1RLM2139C0011","S1RLM2139C0012","S1RLM2139C0014","S1RLM2139C0018","S1RLM2139C0020","S1RLM2139C0023","S1RLM2139C0028","S1RLM2140C0005","S1RLM2140C0027","S1RLM2141C0004","S1RLM2141C0012","S1RLM2141C0014","S1RLM2141C0032","S1RLM2142C0001","S1RLM2142C0009","S1RMM2124C0005","S1RMM2124C0019","S1RMM2142C0008","S1RMM2146C0043","S1RMM2146C0044","S1RMM2146C0045","S1RMM2147C0009","S1RMM2147C0024","S1RMM2147C0025","S1RMM2208C0026","S1RMM2208C0033","S1RMM2208C0035","S1RMM2210C0001","S1RMM2210C0002","S1RMM2210C0005","S1RMM2210C0007","S1RMM2210C0011","S1RMM2211C0003","S1RMM2211C0004","S1RMM2211C0008","S1RMM2211C0029","S1RMM2211C0036","S1RMM2211C0040","S1RMM2211C0047","S1RMM2246C0016","S1RMM2247C0001","S1RMM2247C0023","S1RMM2247C0033","S1RMM2247C0035","S1RMM2247C0046","S1RMM2247C0054","S1RMM2247C0058","S1RMM2247C0066","S1RMM2247C0067","S1RMM2247C0068","S1RMM2247C0077","S1RMM2248C0001","S1RMM2248C0004","S1RMM2248C0010","S1RMM2248C0026","S1RMM2248C0038","S1RMM2320C0004","S1RMM2320C0010","S1RMM2320C0021","S1RMM2320C0022","S1RMM2323C0014","S1RMM2324C0001","S1RMM2324C0013","S1RMM2324C0027","S1RMM2324C0029","S1RMM2324C0041","S1RMM2324C0046","S1RMM2324C0050","S1RMM2329C0002","S1RMM2329C0060","S3RAM2211C0004","S3RAM2211C0010","S3RAM2212C0009","S3RAM2212C0020","S3RAM2212C0025","S3RAM2212C0027","S3RAM2212C0028","S3RAM2212C0033","S3RAM2225C0006","S3RAM2225C0040","S3RAM2225C0042","S3RAM2225C0051","S3RAM2225C0053","S3RAM2225C0081","S3RAM2225C0084","S3RAM2225C0089","S3RAM2225C0093","S3RAM2225C0105","S3RAM2225C0126","S3RAM2225C0128","S3RAM2236C0002","S3RAM2236C0023","S3RAM2236C0047","S3RAM2236C0065","S3RAM2236C0080","S3RAM2236C0083","S3RAM2236C0088","S3RAM2236C0089","S3RAM2236C0114","S3RAM2236C0118","S3RAM2236C0119","S3RAM2236C0125","S3RAM2236C0131","S3RAM2236C0132","S3RAM2236C0137","S3RAM2236C0140","S3RAM2244C0012","S3RAM2244C0022","S3RAM2244C0028","S3RAM2244C0030","S3RAM2244C0049","S3RAM2244C0055","S3RAM2244C0069","S3RAM2244C0076","S3RAM2244C0079","S3RAM2244C0083","S3RAM2245C0001","S3RAM2245C0008","S3RAM2245C0019","S3RAM2245C0024","S3RAM2245C0038","S3RAM2245C0043","S3RAM2245C0048","S3RAM2245C0076","S3RAM2245C0087","S3RAM2245C0096","S3RAM2251C0002","S3RAM2251C0003","S3RAM2252C0004","S3RAM2252C0025","S3RAM2252C0030","S3RAM2252C0032","S3RAM2252C0048","S3RAM2252C0049","S3RAM2252C0051","S3RAM2252C0058","S3RAM2252C0074","S3RAM2252C0084","S3RAM2319C0018","S3RAM2319C0022","S3RAM2320C0002","S3RAM2320C0006","S3RAM2320C0010","S3RAM2320C0019","S3RAM2325C0001","S3RAM2325C0002","S3RAM2325C0005","S3RAM2325C0006","S3RAM2325C0008","S3RAM2325C0016","S3RAM2325C0018","S3RAM2325C0025","S3RAM2325C0050","S3RAM2325C0056","S3RAM2325C0061","S3RAM2325C0064","S3RAM2325C0074","S3RAM2325C0085","S3RAM2325C0092","S3RAM2325C0093","S3RAM2325C0102","S3RAM2325C0112","S3RAM2327C0014","S3RAM2327C0015","S3RAM2327C0017","S3RAM2327C0075","S3RAM2328C0001","S3RAM2328C0016","S3RAM2328C0017","S3RAM2328C0023","S3RAM2328C0025","S3RAM2328C0026","S3RAM2328C0035","S3RAM2328C0036","S3RAM2328C0041","S3RAM2328C0044","S3RAM2328C0052","S3RAM2328C0085","S3RAM2328C0089","S3RAM2328C0093","S3RAM2328C0094","S3RAM2328C0099","S3RAM2328C0109","S3RAM2328C0119","S3RAM2329C0005","S3RAM2329C0014","S3RAM2329C0016","S3RAM2329C0020","S3RAM2329C0021"]
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
    cat /data/logs/anr/$f | head -n5 | grep "Cmd line"
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
    if sub_topic is None:
        return
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
                    cnt += 1
                    if cnt > 3:
                        clean_and_unsubscribe()
                        index = 0
                        break
                except KeyboardInterrupt:
                    print(f"Interrupted by user, skipping...{robot_id}")
                    clean_and_unsubscribe()
                    index = 0
                    break
        print(f"Finished!")
        while True:
            pass
    except KeyboardInterrupt:
        close_connection()
        print("Disconnected and stopped the loop.")
        print(aeskey)
