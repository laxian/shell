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
  -H 'Cookie: JSESSIONID=6D0128851A80C90B015458DD2BA6AA6D; bad_idf05eae40-9a31-11e5-83f6-57006c315d67=08948f20-6279-11ea-9412-319fe6106bd3; href=http%3A%2F%2Fninebot.21tb.com%2Fos%2Fhtml%2FdeskTop.init.do; nice_idf05eae40-9a31-11e5-83f6-57006c315d67=9651e221-fe57-11ea-a8de-e9074b759bc0; corp_code=ninebot; nxYongdaoIp=10.0.1.152; changId=39ee9023395e78171e0eabf6c35d7103; eln_session_id=elnSessionId.fc6f456eb60d4e4d98f3265bcea18d44; qimo_seosource_f05eae40-9a31-11e5-83f6-57006c315d67=%E7%AB%99%E5%86%85; qimo_seokeywords_f05eae40-9a31-11e5-83f6-57006c315d67=; accessId=f05eae40-9a31-11e5-83f6-57006c315d67; pageViewNum=5' \
  --data-raw 'creditQueryType=true&timeType=LATELY_ONE_WEEK' \
  --compressed \
  --insecure \
  |sed -e "s#.*elsCourseScore\":\"\([0-9]\+\.[0-9]\).*#已学：\1 小时\n#g"