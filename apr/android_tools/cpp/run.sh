#!/usr/bin/env bash


$ANDROID_HOME/cmake/3.6.4111459/bin/cmake -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI=arm64-v8a
adb push HelloWorld /data/local/tmp 
adb shell /data/local/tmp/HelloWorld