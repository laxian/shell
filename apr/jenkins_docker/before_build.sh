#!/usr/bin/env bash -x

echo "------ before gradle build ------"
if [ $use_aliyun_maven = true ]; then
    sed -i "/repositories {/a \ \t\tmaven { url 'https://maven.aliyun.com/repository/google' }" build.gradle
    sed -i "/repositories {/a \ \t\tmaven { url 'https://maven.aliyun.com/repository/jcenter' }" build.gradle
fi
if [ $JOB_NAME == "Gx_Service" ]; then
    sed -i "s;3.+;5.3.0;g" build.gradle
    echo "/opt/app/android-sdk/ndk/22.0.7026061" >> local.properties
fi
if [ $JOB_NAME == "nav_app-debug" ]; then
    echo "sdk.dir=/opt/app/android-sdk" > local.properties
    echo "ndk.dir=/opt/app/android-sdk/ndk/16.1.4479499" >> local.properties
    git submodule update --init --recursive
    python3 -m pip install -r ./sdk/trident_ftp/requirements.txt
    ./gradlew sdk:algobase:assemble
fi

GIT_COUNT=$(git rev-list HEAD --first-parent --count)
VERSION_NAME=1.0.${GIT_COUNT}
VERSION_CODE=10000${GIT_COUNT}
echo $GIT_COUNT
sed -i "s/versionCode.*/versionCode $VERSION_CODE/g" app/build.gradle
sed -i "s/versionName.*/versionName \"$VERSION_NAME\"/g" app/build.gradle

echo "------ after gradle build ------"
