#!/usr/bin/env bash

#----------------------------------------------------------------
# 使用国内镜像下载gradle distributeUrl并部署
# ./main.sh <android_project_root>
#----------------------------------------------------------------

GRADLE_USER_HOME=$HOME/.gradle
GRADLE_WRAPPER_PATH="wrapper/dists"
GRADLE_DIST_PATH=$GRADLE_USER_HOME/$GRADLE_WRAPPER_PATH

SCRIPT_PATH="gradle/wrapper"
SCRIPT_NAME="gradle-wrapper.properties"

project_path=$1
gradle_file=$1/$SCRIPT_PATH/$SCRIPT_NAME

url=$(grep distributionUrl $gradle_file | sed 's/distributionUrl=//g; s/https\\/https/g')
name=${url##*/}
name_no_ext=${name/.zip/}
gradle_version=${name%-*}

mirror_host="https://mirrors.cloud.tencent.com/gradle"
mirror_url=$mirror_host/$name

hash=$(python hash.py $url)
zip_output=$GRADLE_DIST_PATH/$name_no_ext/$hash

if [ -f $zip_output/$name.ok ]; then
    echo $zip_output already exists!
    $project_path/gradlew -p $project_path
else
    [ -f $name ] || curl -OL $mirror_url
    mkdir -p $zip_output
    [ -d $zip_output/$gradle_version ] || unzip $name -d $zip_output
    touch $zip_output/$name.ok
    touch $zip_output/$name.lck
    echo "gradle setup success!"
    $project_path/gradlew -p $project_path
fi
