import poplib
from email.header import decode_header
from email.parser import Parser
import re
import html
import urllib.parse
import sys


# 邮件地址, 口令和POP3服务器地址:
download_email = '${mail}'
password = '${qy_163_token}'
pop3_server = 'pop.qiye.163.com'

server = poplib.POP3_SSL(pop3_server)
server.user(download_email)
server.pass_(password)

filter_str = "D2_System_Dev_1.1.551"
if len(sys.argv) > 1:
    filter_str = sys.argv[1]

def decode_str(aStr):
    """
    字符编码转换
    """
    # decode_header方法会将字符串还原成二进制 并获取该字符串的正确解析方式
    # 返回值：[(bytes,charset)]
    bytes, charset = decode_header(aStr)[0]
    if charset:
        value = bytes.decode(charset)
        return value
    else:
        return None


# 获取所有邮件item
resp, mails, octets = server.list()

print(len(mails))
for i in range(len(mails), 0, -1):
    # resp:响应 lines:每一行的数据组成的列表 octets:邮件大小
    try:
        resp, lines, octets = server.retr(i)
    except Exception as ex:
        print(ex)
        continue
    # 换行符拼接二进制文件 并utf-8解码，忽略其中有异常的编码，仅显示有效的编码
    msg_content = b'\r\n'.join(lines).decode('utf-8', 'ignore')
    # if "Interaction_System_DEV" not in msg_content:
    #     continue
    # 将字符串转化为Message对象
    msg = Parser().parsestr(msg_content)
    # 邮件标题
    from_addr = msg.get('From')
    expect_from = 'app-test-mail@ninebot.com'
    if expect_from not in from_addr:
        # print(from_addr)
        continue
    subject = decode_str(msg.get('Subject'))
    if not subject:
        continue
    # print(subject)
    if subject is not None and filter_str in subject:
        for part in msg.walk():
            # print(type(part) )
            if part.get_content_type() != "text/html":
                continue
            
            page=part.as_string()

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
        print("\r\n".join(li_list))
        break

