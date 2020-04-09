#!/usr/bin/python

import sys
import re


__author__ = 'zwx'

def procceed_line(line):
    m = p.search(line)
    if m is not None:
        num = m.group('num')
        # print ('%s -> %.1f' % (num, float(num) * 1.5))
        newline = line.replace(num, str(float(num) * 1.5))
        # print(newline)
        return newline
    else:
        # print ("not found")
        return line


if __name__ == '__main__':

    # 从命令行读取被处理文件路径
    path = sys.argv[1]
    # test_line = 'android:layout_width="346dp"'

    # 正则，匹配格式： 123.24dp
    r = '(?P<num>\d+(\.\d+)?)dp'
    p = re.compile(r)

    input_file = open(path, 'r+')
    lines = input_file.readlines()
    input_file.truncate()
    input_file.seek(0)
    for l in lines:
        newline = procceed_line(l)
        print(newline)
        input_file.write(newline)

    input_file.close()
