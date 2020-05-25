#!/usr/bin/env bash -x

# alpha dev internal release
CUBE_ENV=
DEVICE_ID=
ROBOT_ID=
ROBOT_KEY=

PROJ_ROOT=.
HOST_FILE=app/src/main/java/com/ssssss/robot/cabinet/http/RxHttp.java
PKG_NAME=com.ssssss.robot.cabinet
CONFIG_FILE='{"NavServicURL":"SSL_PATH","EnableLog":true}'
HOST_PATTERN="https\?://[a-z-]\+\.lllll\.com"
CONFIG_PATH=/sdcard/GX/config.json

HOST_ALPHA=http://alpha-cube.lllll.com
SSL_ALPHA=ssl://000.92.80.43:8884
HOST_DEV=http://dev-cube.lllll.com
SSL_DEV=ssl://000.131.2.136:8884
HOST_INTERNAL=http://internal-cube.lllll.com
SSL_INTERNAL=ssl://000.131.2.136:8885
HOST_RELEASE=http://cube.lllll.com
SSL_RELEASE=ssl://000.131.12.142:8884
# alpha debug release
APK_DIR=alpha

if [ $CUBE_ENV = "alpha" ]; then
    HOST=$HOST_ALPHA
    SSL=$SSL_ALPHA
elif [ $CUBE_ENV = "dev" ]; then
    HOST=$HOST_DEV
    SSL=$SSL_DEV
elif [ $CUBE_ENV = "internal" ]; then
    HOST=$HOST_INTERNAL
    SSL=$SSL_INTERNAL
elif [ $CUBE_ENV = "release" ]; then
    HOST=$HOST_RELEASE
    SSL=$SSL_RELEASE
fi

if [ $CUBE_ENV = "internal" ]; then
    APK_DIR=release
elif [ $CUBE_ENV = "dev" ]; then
    APK_DIR=debug
else
    APK_DIR=$CUBE_ENV
fi

# 修改host
sed -i "/String host/s#$HOST_PATTERN#$HOST#g" $PROJ_ROOT/$HOST_FILE

# build
pushd $PROJ_ROOT
if [ $CUBE_ENV = "alpha" ]; then
    $PROJ_ROOT/gradlew clean assembleAlpha
elif [ $CUBE_ENV = "dev" ]; then
    $PROJ_ROOT/gradlew clean assembleDebug
else
    $PROJ_ROOT/gradlew clean assembleRelease
fi
popd

# install
adb -s $DEVICE_ID uninstall $PKG_NAME
adb -s $DEVICE_ID install -r $PROJ_ROOT/app/build/outputs/apk/$APK_DIR/*.apk

# config MQTT ssl
echo $CONFIG_FILE | sed "s#SSL_PATH#$SSL#g" > config.json
adb -s $DEVICE_ID push config.json $CONFIG_PATH
rm config.json

# set robot_id/robot_key
adb -s $DEVICE_ID shell settings put secure robot_id $ROBOT_ID
adb -s $DEVICE_ID shell settings put secure robot_key $ROBOT_KEY

# reboot device
adb -s $DEVICE_ID reboot
