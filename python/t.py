import time
import os

path='/Users/leochou/Downloads/com.segway.robot.algo.${host_part_2}go_nav_app/'

def isToday(tstr):
    now = time.localtime()
    lt = time.strptime(tstr, '%Y-%m-%d_%H-%M-%S_%f')
    return now.tm_mday == lt.tm_mday and now.tm_mon == lt.tm_mon and now.tm_year == lt.tm_year


def isYesterday(tstr):
    now = time.localtime()
    lt = time.strptime(tstr, '%Y-%m-%d_%H-%M-%S_%f')
    return now.tm_mday - 1 == lt.tm_mday and now.tm_mon == lt.tm_mon and now.tm_year == lt.tm_year

for d in os.listdir(path):
    if not d.startswith('.') and isYesterday(d):
        print(d)
        print(isToday(d))

