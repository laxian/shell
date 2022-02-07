#!/usr/bin/env bash

# ----------------------------
# 使用aapt打印apk的版本信息
# param 1: path to apk
# ----------------------------

APK_PATH=${1}

if [ -z "$ANDROID_HOME" ]; then
	echo "You must set ANDROID_HOME"
else
	DIR_VER=$(ls $ANDROID_HOME/build-tools/ | tail -1)
	AAPT=$ANDROID_HOME/build-tools/$DIR_VER/aapt2
	if [ -e $AAPT ]; then
		$AAPT dump badging $APK_PATH | grep versionCode
	else
		echo "ERROR: Unable to find executable aapt"
	fi
fi
