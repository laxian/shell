#!/usr/bin/env bash

# echo "url:http://www.baidu.com/a.zip" | grep "http.*\.zip" | sed 's/.*\(http.*\.zip\).*/\1/g' 

echo '                                "logUrl":"http://robot-base.loomo.com/aws/web/file/download/?bucketName=ota-robot-base&objectKey=log/S1RLM2047C0003_2020-12-01_16-05-14-654_M.zip",' \
| grep "http.*\.zip" | tr -d ' ' \
| (test -s /dev/stdin && cat || echo 'pipe is empty')


