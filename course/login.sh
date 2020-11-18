#!/usr/bin/env bash

#----------------------------
# 登录方式获取cookie，用于获取数据
#----------------------------


username=$1
password=$2
tmp=`mktemp`

curl 'https://ninebot.21tb.com/login/login.ajaxLogin.do'\
 -H 'Host: ninebot.21tb.com' \
 -H 'Accept: application/json, text/javascript, */*' \
 -H 'X-Requested-With: XMLHttpRequest' \
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36' \
 -H 'Origin: https://ninebot.21tb.com' \
 -H 'Sec-Fetch-Site: same-origin' \
 -H 'Sec-Fetch-Mode: cors' \
 -H 'Sec-Fetch-Dest: empty' \
 -H 'Referer: https://ninebot.21tb.com/login/login.init.do?returnUrl=https%3A%2F%2Fninebot.21tb.com%2Fels%2Fhtml%2FcourseStudyItem%2FcourseStudyItem.learn.do%3FcourseId%3D3a1473a679574bbdb802086d550424f9%26courseType%3DNEW_COURSE_CENTER%26vb_server%3Dhttp%253A%252F%252F21tb-video.21tb.com&elnScreen=1440*900elnScreen' \
 -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
 --data "corpCode=ninebot&loginName=$username&password=$password&returnUrl=https%3A%2F%2Fninebot.21tb.com%2Fels%2Fhtml%2FcourseStudyItem%2FcourseStudyItem.learn.do%3FcourseId%3D3a1473a679574bbdb802086d550424f9%26courseType%3DNEW_COURSE_CENTER%26vb_server%3Dhttp%253A%252F%252F21tb-video.21tb.com&courseId=&securityCode=&continueLogin=true&hyperEspCode=&md5Password=false" \
 --compressed -vs 2>&1 | grep "Set-Cookie" | sed -e "s#.*Cookie: ##g" > $tmp

 tr '\n\r' ' ' < $tmp > cookie
