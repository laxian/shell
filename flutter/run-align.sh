#!/bin/sh
# by zhouweixian
# 本地plugin的修改，都房子这个shell文件里了。不同用户，需执行一下这个脚本，完成对齐
# sed 用的是 Mac-sed。 gnu-sed 需要做适量修改

if [ -z $1 ]; then
	PROJECT_ROOT=$(pwd)
else
	PROJECT_ROOT=$1
fi

# or gnu-sed
sed=/usr/bin/sed

#gradle wrapper
GRADLE_WRAPPER_PATH=android/gradle/wrapper/gradle-wrapper.properties
GRADLE_WRAPPER_FULLPATH=$PROJECT_ROOT/$GRADLE_WRAPPER_PATH
/usr/bin/sed -i "" "s/gradle-4.4-all/gradle-4.10.2/g" $GRADLE_WRAPPER_FULLPATH

#recorder_wav bugs
RECORD_PATH=/Users/etiantian/flutter/flutter-0.10.0/.pub-cache/hosted/pub.flutter-io.cn/recorder_wav-0.0.1/android/src/main/java/com/bilibili502/recorderwav/AudioUtil.java

sig='recordData();'
sig2='if (recorder.getState() == STATE_UNINITIALIZED) { recorder = new AudioRecord(audioSource, audioRate, audioChannel, audioFormat, bufferSize); }'
sig_ret=$(grep $sig $RECORD_PATH)

rep='startRecording();'
if [ -z $sig_ret ]; then
	echo "INSET after $rep"
	$sed -i "" "/$rep/a\\
    recordData();
    " $RECORD_PATH

	$sed -i "" "/public void startRecord() {/a\\
    $sig2
    " $RECORD_PATH

	$sed -i "" "s/44100/16000/g" $RECORD_PATH
else
	echo 'Already Added'
fi
