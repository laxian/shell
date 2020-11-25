#!/usr/bin/env bash -x


curl 'https://analytics.lexiang-asset.com/report/code_rp' \
  -H 'authority: analytics.lexiang-asset.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'origin: https://lexiangla.com' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://lexiangla.com/' \
  -H 'accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  --data-raw '[{"companyId":"d05406eccd0b11ea8bac5254002f1020","staffId":"6bda4c14d6be11eaad0a0a58ac134369","method":"put","httpCode":200,"pageDomain":"lexiangla.com","url":"lexiangla.com/api/v1/classes/CLASSID/courses/COURSEID/study","path":"/classes/CLASSID/courses/COURSEID/study","time":207,"utime":{TIMESTAMP},"XRequestId":"{UUID}","platform":"pc","isNew":true,"isWafError":0,"code":0,"msg":"success","isAlpha":0,"params":"{\"learn_time\":{LEARN_TIME},\"is_ended\":{IS_ENDED}}"}]' \
  --compressed