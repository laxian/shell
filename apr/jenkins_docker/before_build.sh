#!/usr/bin/env bash

echo "------ before gradle build ------"
if [ $use_aliyun_maven == 'true' ]; then
    sed -i "/repositories {/a \ \t\tmaven { url 'https://maven.aliyun.com/repository/google' }" build.gradle
    sed -i "/repositories {/a \ \t\tmaven { url 'https://maven.aliyun.com/repository/jcenter' }" build.gradle
fi
if [ $JOB_NAME == "Gx_Service" ]; then
    sed -i "s;3.+;5.3.0;g" build.gradle
    echo "/opt/app/android-sdk/ndk/22.0.7026061" >> local.properties
fi
echo "------ after gradle build ------"
