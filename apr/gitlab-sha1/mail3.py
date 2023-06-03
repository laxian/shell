#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import imaplib
import email
from email.header import decode_header

import re
import html
import urllib.parse
import chardet
import sys


# 连接到IMAP服务器
mail = imaplib.IMAP4_SSL("imap.qiye.163.com")

# 登录到邮箱
ret = mail.login("${mail}", "${qy_163_token}")
# print(ret)

# 选择收件箱
ret = mail.select("Inbox")
# 搜索邮件，网易邮箱搜索语法不生效
result, data = mail.search(None, 'ALL')
d=data[0].split()
d.reverse()
print(len(d))

filter_str = "D2_System_Dev_1.1."
if len(sys.argv) > 1:
    filter_str = sys.argv[1]

# show SHA1s or page
mode = 'sha1'
if len(sys.argv) > 2:
    mode = sys.argv[2]

# 遍历搜索结果
for num in d:
    # 获取邮件内容
    result, data = mail.fetch(num, "(RFC822)")
    # print(result, data)
    raw_email = data[0][1]
    if not isinstance(raw_email, int):
        email_message = email.message_from_string(raw_email.decode('utf-8'))
        if not email_message.is_multipart():
            continue
    else:
        pass
        # print(email_message)
    # 解码邮件主题
    subject = decode_header(email_message["Subject"])[0][0]
    fromaddr = decode_header(email_message["From"])[0][0]
    
    if isinstance(subject, bytes):
        # 如果主题是bytes类型，需要进行解码
        subject = subject.decode(chardet.detect(subject)["encoding"])
        if filter_str not in subject:
            continue
        # 输出邮件主题和发件人
        # print("Subject:", subject)
        # print("From:", email_message["From"])
        page=email_message.get_payload()[0].as_string()
        
        # print(type(page))
        
        it = re.finditer(r"=([0-9A-F]{2})", page)
        for match in it: 
            page = page.replace(match.string, match.string.replace('=', '%'))
        page=html.unescape(page)
        page=urllib.parse.unquote(page)
        # print(page)
        li_list=['<html>']
        li_list.append('<h1>'+subject+'</h1>')
        li_list.append('<ul>')
        first_line=None
        for l in page.split('\n'):
            if first_line:
                line = first_line + l
                first_line = None
                li_list.append(line)
            elif "<li" in l:
                first_line=l
        li_list.append('</ul></html>')
        if mode == 'page':
            print("\r\n".join(li_list))
        else:
            # \w.\w.\w+.([0-9a-f]{7})
            it = re.finditer(r"\w.\w.\w+.([0-9a-f]{7})", page)
            for match in it: 
                print(match.group(1))
        
        exit()
    else:
        # 不处理此类邮件
        continue

# 关闭连接
mail.close()
mail.logout()
