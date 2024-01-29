#!/usr/bin/python
# encoding=utf-8

import base64
import M2Crypto
import os
import argparse

# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取当前脚本目录的上层目录
parent_directory = os.path.dirname(script_directory)
# 将当前工作目录更改为当前脚本所在的路径
os.chdir(script_directory)



# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="处理参数")

# 添加选项参数
parser.add_argument("-a", "--add", help="添加一条白名单")
args = parser.parse_args()

if args.add:
    print("添加一条白名单: %s" % args.add)
    wl_file = open('aibox_install_white_list.txt', 'a')
    wl_file.write(args.add + '\n')
    wl_file.close()
else:
    print("没有添加白名单")
    exit(1)


pri_key_file = os.path.join(f"{script_directory}/private", "private.pem")
pub_key_file = os.path.join(f"{script_directory}/private", "public.pem")
private_key_handle = M2Crypto.RSA.load_key(pri_key_file)
public_key_handle = M2Crypto.RSA.load_pub_key(pub_key_file)


wl_file = open('aibox_install_white_list.txt', 'r')
en_file = open('encrypt_data.txt', 'a')
lines = wl_file.readlines()
lines=[l.rstrip() for l in lines]
for line in lines:
    print('------原文 start------')
    print(line)
    encrypt_text = private_key_handle.private_encrypt(line.encode('utf-8'), M2Crypto.RSA.pkcs1_padding)
    b64_encrypt_text = base64.b64encode(encrypt_text).decode('utf-8')
    print('------加密串 start------')
    print(b64_encrypt_text)
    de_b64_encrypt_text = base64.b64decode(b64_encrypt_text.encode('utf-8'))
    b_decrypt_text = public_key_handle.public_decrypt(de_b64_encrypt_text, M2Crypto.RSA.pkcs1_padding)
    decrypt_text = b_decrypt_text.decode('utf-8')
    print('------解密串 start------')
    print(decrypt_text)
    if line == decrypt_text:
        print('------加解密成功，记录在encrypt_data.txt------')
        en_file.write(line + '\n')
        en_file.write(b64_encrypt_text + '\n')
wl_file.close()
