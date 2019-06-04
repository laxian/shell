#!/bin/sh

set -e

flutter build ios --release

# Mock jenkins env.
JOB_NAME=${JOB_NAME-online-wangxiao-ios}
WORKSPACE=${WORKSPACE-.}
BUILD_NUMBER=${BUILD_NUMBER-99}
# DEFAULT VALUE: `git rev-parse --short HEAD`, if in jenkins, GIT_COMMIT is a buildin variant
GIT_COMMIT=${GIT_COMMIT-$(git rev-parse --short HEAD)}
echo $GIT_COMMIT
SERVER_IP="192.168.10.98"
LOCAL_IP=$(ipconfig getifaddr en0)

#APP BASIC INFO
APP_NAME=wangxiao
APP_SCHEME=Runner
WORKSPACE_NAME=Runner
#  VERSION_NAME=`/usr/bin/agvtool mvers -terse1`
VERSION_NAME=$(cat ios/Runner.xcodeproj/project.pbxproj | grep FLUTTER_BUILD_NAME | cut -d' ' -f3 | cut -d';' -f 1 | uniq)
# like 1.0.4.1
BUILD_VERSION=$(cat ios/Runner.xcodeproj/project.pbxproj | grep "FLUTTER_BUILD_NUMBER =" | cut -d' ' -f3 | cut -d';' -f 1 | uniq)

# NEXUS INFO
NEXUS_JENKINS_NAME=jenkins
NEXUS_JENKINS_PASSWD=jenkins20100328
NEXUS_HOST=http://192.168.10.8:18080
NEXUS_DIR=$NEXUS_HOST/nexus/service/local/repositories/EttAppReleases/content/com/online/$APP_NAME/ios/$VERSION_NAME

#DING DING
DING_TOKEN=d7fb2719a1655eb9e067dd549a86385cc7f57e14a056fe52187da85c1adf3159

MAN_TO_NOTIFY='["18612696105","18612167007","18310511388"]'
# build type testflight or adhoc. default: testflight
[[ $1 == adhoc ]] && BUILD_TYPE=adhoc || BUILD_TYPE=testflight

# FILE PATH AND FILE NAME
JENKINS_TIME=$(date +%m%d)
GIT_COMMIT_HASH=${GIT_COMMIT:0:7}
GIT_REV=$(git rev-list HEAD | wc -l | awk '{print $1}')

# like wangxiao-1.0.4.1.adhoc-0531-99-a0efd23-234.ipa
IPA_NAME=$APP_NAME-$BUILD_VERSION-$BUILD_TYPE-$JENKINS_TIME-$BUILD_NUMBER-$GIT_COMMIT_HASH-$GIT_REV.ipa
# like build/ios/online-wangxiao-ios/99
EXPORT_PATH=./build/ios/$JOB_NAME/$BUILD_NUMBER
# make sure "./build/ios/online-wangxiao-ios/99" exists
mkdir -p $EXPORT_PATH
ARCHIVE_PATH=$EXPORT_PATH/$APP_NAME.xcarchive

XCWORKSPACE_PATH=$WORKSPACE/ios/$WORKSPACE_NAME.xcworkspace

# ad-hoc or testflight
if [ $BUILD_TYPE = adhoc ]; then
    echo "adhoc"
    ExportOptionsPlistPath=ios/adhoc-ExportOptions.plist
else
    echo "testflight"
    ExportOptionsPlistPath=ios/ExportOptions.plist
fi
echo "============== archive =================="
xcodebuild archive -workspace $XCWORKSPACE_PATH \
    -scheme $APP_SCHEME \
    -configuration Release \
    -archivePath $ARCHIVE_PATH

#  ipa
echo "==============  =================="
xcodebuild -exportArchive -archivePath $ARCHIVE_PATH \
    -exportPath $EXPORT_PATH \
    -exportOptionsPlist $ExportOptionsPlistPath

echo 'EXPORT PATH: ------>'
echo $EXPORT_PATH
curl -v -u $NEXUS_JENKINS_NAME:$NEXUS_JENKINS_PASSWD --upload-file $EXPORT_PATH/Runner.ipa $NEXUS_DIR/$IPA_NAME

# post to dingtalk
if [ $SERVER_IP = $LOCAL_IP ]; then
    export WEB_DIR=/Users/hawk/Library/apache-tomcat-9.0.17/webapps/app/$VERSION_NAME
    mkdir -p $WEB_DIR
    host=http://$SERVER_IP:8081/app/$VERSION_NAME
    cp $EXPORT_PATH/Runner.ipa $WEB_DIR/$IPA_NAME
    title="iOS $VERSION_NAME 最新打包预览,点击下载\n"
    content=$title$host/$IPA_NAME

    # 钉钉机器人，手机号为钉钉群里你要@的人的手机号
    pre='{"msgtype":"text","text":{"content":"'
    post='"},"at":{"atMobiles":'$MAN_TO_NOTIFY',"isAtAll":false}}'
    json=$pre$content$post
    echo $json

    curl "https://oapi.dingtalk.com/robot/send?access_token=$DING_TOKEN" -H 'Content-Type: application/json' -d $json
fi
