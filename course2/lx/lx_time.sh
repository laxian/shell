#!/usr/bin/env bash

COOKIE="company_code=d05406eccd0b11ea8bac5254002f1020; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDM4MTMwOTEsImp0aSI6IjUzZTY0OWQyMjQyMDQ0N2M5ZTg3ZmI2NGRhMzYxYjFhIiwiaWF0IjoxNjAxMjIxMDkxLCJpc3MiOiJsZXhpYW5nbGEuY29tIiwibmJmIjoxNjAxMjIxMDgxLCJzdWIiOiJmZGQ1Mzk3ZWZlNTcxMWVhOWQwMjdlZjYxMzM3N2JmMiJ9.96clgmX64Vmf5MXKTg1xo6xRU-H1aD9S9CZtz8SomxI; expires_in=1603813091; company_server_type=lexiang; company_display_name=; ONEAPM_BI_sessionid=2159.216|1601315355387|çº³æ©åï¼åäº¬-å¨å«è´¤; XSRF-TOKEN=B5rTCwQgUGHXoP9u3AdC4BbxBagE76II3GdO9%252Btd%252ButtbOrpC0Jf25Ci8nzfFunxamI5zVo%252Fb41sHL%252F3JYjoB0VgQWxTx7l4kB1WM7U6K1Q%253D"

json=$(curl \
-H 'Host: lexiangla.com' \
-H "Cookie: $COOKIE" \
-H 'accept: application/json, text/plain, */*' \
-H 'x-xsrf-token: B5rTCwQgUGHXoP9u3AdC4BbxBagE76II3GdO9%2Btd%2ButtbOrpC0Jf25Ci8nzfFunxamI5zVo%2Fb41sHL%2F3JYjoB0VgQWxTx7l4kB1WM7U6K1Q%3D' \
-H 'x-requested-with: XMLHttpRequest' \
-H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
-H 'isajax: true' \
-H 'sec-fetch-site: same-origin' \
-H 'sec-fetch-mode: cors' \
-H 'sec-fetch-dest: empty' \
-H "referer: https://lexiangla.com/classes/$1?type=0&company_from=d05406eccd0b11ea8bac5254002f1020" \
-H 'accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
--compressed \
"https://lexiangla.com/api/v1/classes/$1")

course_id=`echo $json | sed -e "s#.*course_id\":\"\([0-9a-f]\+\).*#\1#g"`
time=`echo $json | sed -e "s#.*learn_time\":\([0-9]\+\).*#\1#g"`
duration=`echo $json | sed -e "s/videos.*$//g" -e "s#.*\"duration\":\([0-9]\+\).*#\1#g"`

echo -n $course_id:
echo -n $time:
echo $duration