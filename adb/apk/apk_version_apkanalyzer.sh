#!/usr/bin/env bash

# ----------------------------
# 使用apkanalyzer打印apk的版本信息
# 实际测试，aapt/aapt2更高效
# ----------------------------

APK_PATH=${1}

if [ -z "$ANDROID_HOME" ]; then
	echo "You must set ANDROID_HOME"
else
	if [ -e $ANDROID_HOME/tools/bin/apkanalyzer ]; then
		$ANDROID_HOME/tools/bin/apkanalyzer manifest print $APK_PATH | grep version
	else
		echo "Unable to find executable apkanalyzer tool."
	fi
fi