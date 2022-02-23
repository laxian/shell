#!/usr/bin/env bash

# ----------------------------
# 查看data下面的sssss安装包
# adb安装的路径在data下，系统内置的在oem下
# ----------------------------

adb shell pm list package | grep sssss | awk -F: '{print $2}' | xargs -n 1 -II adb shell pm path I | grep data