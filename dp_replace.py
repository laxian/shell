#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="346dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="519.0dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="519.0dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="778.5dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="519.0dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="778.5dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="778.5dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
#!/usr/bin/python

import sys
import re

path = sys.argv[0]
# regex = sys.argv[1]
# replacement = sys.argv[2]
test_line = 'android:layout_width="1167.75dp"'
r = '(?P<num>\d+(\.\d+)?)dp'
p = re.compile(r)

input_file = open(path, 'r+')


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

for l in input_file.readlines():
    newline = procceed_line(l)
    print(newline)
    input_file.write(newline)

input_file.close()

# procceed_line(test_line)
