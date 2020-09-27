#!/usr/bin/env bash

# ----------------------------
# 获取最近一周已学课程小时数
# ----------------------------

curl -s 'http://ninebot.21tb.com/rtr/html/studentsituation/studentsituation.elsSituation.do' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Accept: */*' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: http://ninebot.21tb.com' \
  -H 'Referer: http://ninebot.21tb.com/rtr/html/index.parserIframe.do?id=0022' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Cookie: YOUR_COOKIE' \
  --data-raw 'creditQueryType=true&timeType=LATELY_ONE_WEEK' \
  --compressed \
  --insecure \
  |sed -e "s#.*elsCourseScore\":\"\([0-9]\+\.[0-9]\).*#已学：\1 小时\n#g"