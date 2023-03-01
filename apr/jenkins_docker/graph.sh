#!/bin/bash -x

# 用于在非Jenkins环境使用
[ ! $JENKINS_HOME ] && {
        export ANDROID_HOME=/opt/app/android-sdk
        export JAVA_HOME=/usr/local/openjdk-8
        export PATH=$JAVA_HOME/bin:$PATH
        sign=true
}

workdir=$(
        cd $(dirname $0)
        pwd
)

GRADLE=build.gradle
PROJ_PATH=${1:-.}

# 添加依赖
sed -i '/^buildscript/{:x N;s/\n\}/&\n\nplugins {\n\tid "com.savvasdalkitsis.module-dependency-graph" version "0.10"\n}/;T x}' ${PROJ_PATH}/${GRADLE}
# 后置apply from
sed -i '/apply from/{H;d};$G' ${PROJ_PATH}/${GRADLE}
# ./gradlew graphModules

# apply plugin语法更新: 添加到plugins{}
TMP_FILE=`mktemp`
sed -n 's/apply plugin: \{.*\}/\tid \1/w ${TMP_FILE}' ${PROJ_PATH}/${GRADLE}
sed -i -e '/plugins/r ${TMP_FILE}' -e '/apply plugin/d' ${PROJ_PATH}/${GRADLE}
rm ${TMP_FILE}

pushd ${PROJ_PATH}
JENKINS_HOME=/var/jenkins_home
outdir=$JENKINS_HOME/outputs/img
png=`./gradlew graphModules | grep .png | awk -F 'at: ' '{print $2}'`
popd

echo $png
time=$(date "+%Y-%m-%d_%H_%M_%S")
picname="${time}-`basename $png`"
mv $png "$outdir/$picname"
host="${host}:8080"
url=http://$host/files/img/$picname
echo $url

tokens=$(cat ./private/token)
. $workdir/utils/notify_img.sh
for token in $tokens; do
	echo $token "---" "--" $url
	wechat_notify $token "---" "--" $url
done
