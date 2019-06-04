#!/bin/sh

set -e

echo $BUILD_URL
echo $JOB_URL
echo $WORKSPACE

VERSION_NAME=$(cat ./android/local.properties | grep versionName | cut -d'=' -f2)

LOCAL_IP=$(ipconfig getifaddr en0)

APK_PATH=app/$VERSION_NAME

WEBAPP_DIR=/Users/hawk/Library/apache-tomcat-9.0.17/webapps

SHARE_HOST=http://$LOCAL_IP/$APK_PATH

WEB_DIR=$WEBAPP_DIR/$APK_PATH

ETT_APP_NAME=wangxiao

NEXUS_HOST=http://192.168.10.8:18080
NEXUS_DIR=$NEXUS_HOST/nexus/service/local/repositories/EttAppReleases/content/com/online/$ETT_APP_NAME/android/$VERSION_NAME

NEXUS_JENKINS_NAME=jenkins
NEXUS_JENKINS_PASSWD=jenkins20100328

ETT_PACKAGE_PATH=$WORKSPACE/build/app/outputs/apk

DING_TOKEN=d7fb2719a1655eb9e067dd549a86385cc7f57e14a056fe52187da85c1adf3159

MEN_TO_NOTIFY='["18501378653","18612167007","18310511388"]'

flutter packages get
flutter clean
flutter build apk --release -v --flavor develop
# cd android

gradle -v
# gradle -pandroid -Pchannel -Pverbose=true -Ptarget=lib/main.dart -Ptrack-widget-creation=false -Pcompilation-trace-file=compilation.txt -Ptarget-platform=android-arm assembleRelease -xlint
gradle clean build -Pchannel -pandroid -xlint

content="Android $VERSION_NAME 最新打包预览,点击下载\n"
function getdir() {
    echo $1
    for file in $1/*; do
        if test -f $file; then
            # echo $file
            arr=(${arr[*]} $file)

            if [ "${file##*.}"x = "apk"x ]; then
                echo "found" $file
                name=$(basename $file)
                echo name
                curl -v -u $NEXUS_JENKINS_NAME:$NEXUS_JENKINS_PASSWD --upload-file $file $NEXUS_DIR/$name

                cp $file $WEB_DIR/
                content=$content$SHARE_HOST/$(basename $file)'\n'
                echo ---
                echo $content
                echo ---
            fi
        else
            getdir $file
        fi
    done

}
getdir $ETT_PACKAGE_PATH
# echo  ${arr[@]}

# 钉钉机器人，手机号为钉钉群里你要@的人的手机号
pre='{"msgtype":"text","text":{"content":"'
post='"},"at":{"atMobiles":'$MEN_TO_NOTIFY',"isAtAll":false}}'
json=$pre$content$post
echo $json

curl 'https://oapi.dingtalk.com/robot/send?access_token=$DING_TOKEN' -H 'Content-Type: application/json' -d $json
