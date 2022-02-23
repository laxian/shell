#!/usr/bin/env bash

# ----------------------------
# $1 接收一个参数用于关键字过滤，可空，表示不过滤
# 依赖adb连接
# ----------------------------

if [ -z $1]; then
	adb shell tail -f /sdcard/logs_folder/com.github.megatronking.netbare.sample/$(adb shell ls -t /sdcard/logs_folder/com.github.megatronking.netbare.sample | head -1)
if [ $1 = tcp ]; then
	adb shell tail -f /sdcard/logs_folder/com.github.megatronking.netbare.sample/$(adb shell ls -t /sdcard/logs_folder/com.github.megatronking.netbare.sample | head -1) | grep TCP
elif [ $1 = url ]; then
	adb shell tail -f /sdcard/logs_folder/com.github.megatronking.netbare.sample/$(adb shell ls -t /sdcard/logs_folder/com.github.megatronking.netbare.sample | head -1) | grep URL
else
	adb shell tail -f /sdcard/logs_folder/com.github.megatronking.netbare.sample/$(adb shell ls -t /sdcard/logs_folder/com.github.megatronking.netbare.sample | head -1) | grep $1
fi
