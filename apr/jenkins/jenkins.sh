#!/bin/bash -ex

SERVICE_ALL_APK=~/Work/app-apr-food-deliver/app/build/outputs/apk/alpha/

# upload
upload_url=http://localhost:8082/upload-jenkins
suffix=apk
for file in $SERVICE_ALL_APK/*; do
    if test -f $file; then
        if [ "${file##*.}"x = ${suffix}x ]; then
            curl -u file:file -F "file=@$file" $upload_url/$DATE
        fi
    fi
done

# notify
token=b9317217-943d-4d1d-9ea6-9a576bc013ee
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token
# archive_url=http://localhost/share/
# nexus_url=http://localhost:8081/#browse/browse:rawrepo
resty_url=http://localhost:8082/files/jenkins/

content="<font color = \\\"info\\\">【$JOB_NAME】</font>构建<font color=\\\"info\\\">成功~</font>😊\n>[查看控制台](${BUILD_URL}console) \n>版本: <font color=\\\"info\\\">${version}</font> \n>commit: <font color=\\\"info\\\">${git_version}</font> \n>存档: - [resty](${resty_url})"

json="{
        \"msgtype\": \"markdown\",
        \"markdown\": {
            \"content\": \"$content\"
        }
   }"

echo $json

curl $notify_url \
    -H 'Content-Type: application/json' \
    -d "$json"
