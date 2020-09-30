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
  -H 'Cookie: corp_code=ninebot; nxYongdaoIp=10.0.1.152; href=http%3A%2F%2Fninebot.21tb.com%2Fels%2Fhtml%2Findex.parser.do%3Fid%3DNEW_COURSE_CENTER%26current_app_id%3D8a80810f5ab29060015ad1906d0b3811; accessId=f05eae40-9a31-11e5-83f6-57006c315d67; bad_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c01-00a3-11eb-aea2-1f1941c69e04; nice_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c02-00a3-11eb-aea2-1f1941c69e04; qimo_seosource_f05eae40-9a31-11e5-83f6-57006c315d67=%E7%AB%99%E5%86%85; qimo_seokeywords_f05eae40-9a31-11e5-83f6-57006c315d67=; changId=24b607e92a8bd889a3a478e548cf7d91; eln_session_id=elnSessionId.f6e5ff7b82874997b3acc096042508f3; pageViewNum=9' \
  --data-raw 'creditQueryType=true&timeType=LATELY_ONE_WEEK' \
  --compressed \
  --insecure \
  |sed -e "s#.*elsCourseScore\":\"\([0-9]\+\.[0-9]\).*#已学：\1 小时\n#g"