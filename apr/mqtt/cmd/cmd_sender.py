#!/usr/bin/env python3


#
#

import paho.mqtt.client as mqtt
import ssl
import uuid
from cmd_message import CmdMessage  # 导入 CmdMessage 类
from cmd_inner_message import CmdMessageInner  # 导入 CmdMessageInner 类
from rsa import (
    rsa_decrypt,
    rsa_sign_sha1,
    rsa_encrypt,
    load_private_key_from_file,
    load_public_key_from_file,
)  # 导入 CmdMessageInner 类

from dec import decryption
from aes2 import aes_encrypt, aes_decrypt, aes_decrypt_java, aes_encrypt_java
import os
import sys
import json
import base64


sys.path.append(".")

pri_key_path = os.path.join("./private", "private.pem")
pub_key_path = os.path.join("./private", "public.pem")
pubkey = load_public_key_from_file(pub_key_path)
prikey = load_private_key_from_file(pri_key_path)

# MQTT参数
username = "${username}"
password = "${cipher}"  # Replace with your actual password
client_id = "zwx2"
broker_address = "${host}"
broker_port = 13080
sub_topic = "robot/S3RAM2225C0003/log/cmd/send"
pub_topic = "robot/S3RAM2225C0003/log/cmd/command"

# SSL证书和密钥文件
ca_file = "../ca_crt"
client_cert = "../client_crt"
client_key = "../client_key"

aeskey = None


# 连接回调
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅主题
    client.subscribe(sub_topic)


# 消息接收回调
def on_message(client, userdata, msg):
    json_object = json.loads(msg.payload.decode("utf-8"))
    content = json_object["responce"]
    if json_object["commandType"] == "verified":
        print("---------------- VERIFIED ----------------")
        print(json_object['responce'])

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
        print("---------------- doRSA ----------------")
        content = json_object["responce"]
        print(content)

    elif json_object["commandType"] == "execute":
        print("---------------- execute ----------------")
        print(content)
        if content.startswith("start handle message"):
            raw = content.split('\'')
            aes = raw[5].strip()
            print(f"AES: {aes}")
            dec = aes_decrypt_java(aes, aeskey)
            print(f"Decrypted: {dec}")
            
    else:
        print(f"Received message: {json_object['commandType']}")


def make_message(cmd):
    global aeskey
    inner = CmdMessageInner()
    inner.set_command(cmd)
    inner_str = json.dumps(inner.to_dict())
    print(inner_str)
    # print(type(aes_encrypt(inner_str.encode(), aeskey.encode())))
    # en_inner_str = base64.b64decode(
    #     aes_encrypt(inner_str.encode(), aeskey.encode())
    # )
    en_inner_str = aes_encrypt_java(inner_str, aeskey)
    print(f"Encrypted inner message: {en_inner_str}")
    print(en_inner_str)
    message_payload = CmdMessage(command_type="execute", cmd_message_inner=en_inner_str)
    return message_payload


def send_message(client, msg):
    message_payload = make_message(msg)
    payload = json.dumps(message_payload.to_dict())
    print('================================ SEND ===================================')
    print(payload)
    print('============================== SEND END =================================')
    client.publish(pub_topic, payload=payload, qos=1)


# 创建MQTT客户端
client = mqtt.Client(client_id)
client.username_pw_set(username, password)
client.tls_set(
    ca_certs=ca_file, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_NONE
)  # 设置不验证服务器证书
client.on_connect = on_connect
client.on_message = on_message

# 连接到Broker
client.connect(broker_address, broker_port)

# 循环处理消息
client.loop_start()

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

# 持续运行，等待消息
try:
    while True:
        cmd = input('->  ')
        send_message(client, cmd)
        pass
except KeyboardInterrupt:
    client.unsubscribe(sub_topic)
    # client.unsubscribe(pub_topic)
    client.disconnect()
    client.loop_stop()
    print("Disconnected and stopped the loop.")
    print(aeskey)
