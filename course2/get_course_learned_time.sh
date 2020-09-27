#!/usr/bin/env bash -x

#----------------------------
# 获取页面内已学时长元素值
#----------------------------

curl -s $1  \
-H 'Cookie: YOUR_COOKIE' \
| grep "studiedTime = " | sed -e "s#.*studiedTime = \([0-9]\+\).*#\1#g"