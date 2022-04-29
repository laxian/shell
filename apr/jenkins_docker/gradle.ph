#!/usr/bin/env bash -x

# --------------------------------
# 企业微信机器人图文消息通知
# ./notify_img.sh <token> <title> <subtitle> <url> [picUrl=url]
# --------------------------------


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
./gradlew graphModules
popd
