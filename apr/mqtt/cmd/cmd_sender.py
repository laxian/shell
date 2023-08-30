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


# 连接回调
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅主题
    # client.subscribe(sub_topic)


def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed with result code {mid}")
    send_verify()


# 消息接收回调
def on_message(client, userdata, msg):
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
        send_message(client, "settings get secure robot_id")
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

    else:
        print(f"Received message: {json_object['commandType']}")


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
    print("================================ SEND ===================================")
    print(payload)
    print("============================== SEND END =================================")
    client.publish(pub_topic, payload=payload, qos=1)


def send_verify():
    # 发布消息
    # message_payload = '{"commandId":1,"commandType":"doRSA","mCmdMessageInner":"pwd"}'
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
    print(f"Subscribing to {sub_topic}")
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


if __name__ == "__main__":

    connect_to_broker()

    # 持续运行，等待消息
    try:
        while True:
            cmd = input(f"{robot_id} -> " if robot_id else "->  ")
            if cmd == "exit":
                close_connection()
                print("Disconnected and stopped the loop.")
                exit(0)
            if client.is_connected():
                if robot_id is None:
                    if cmd.startswith("S") or cmd.startswith("GXBOX-"):
                        robot_id = cmd.strip()
                        subscribe_robot(robot_id)
                    else:
                        print("Please input robot id first.")
                elif cmd == "q":
                    client.unsubscribe(sub_topic)
                    robot_id = None
                elif not cmd:
                    pass
                else:
                    send_message(client, cmd)
            else:
                print("Not connected to broker.")
                print("Reconnecting...")
    except KeyboardInterrupt:
        close_connection()
        print("Disconnected and stopped the loop.")
        print(aeskey)
