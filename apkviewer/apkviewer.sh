#!/bin/bash

# 反编译apk
# 1、使用apktool反编译资源
# 命令格式：apktool d <apk_file>
# 2、使用unzip解压缩apk包
# unzip -q <apk_file> -d <out_dir>
# 3、使用dex2jar将dex转换成jar文件
# dex2jar <dex_file>
# 4、使用jadx-gui分别打开jar文件

# 配置反编译工具路径
# apktool=$JD_HOME/apktool
dex2jar=/usr/local/bin/d2j-dex2jar
jdgui=/usr/local/bin/jd-gui

log() {
	echo -e "$1:\t$2"
}

# 判断是否是http地址
# if true return 1 else 0
is_url() {
	
	url=$1
	len=${#url}
	if [ $len -lt 8 ]; then
		return 0
	else
		start=${url:0:7}
		if [ $start = "http://" ]; then
			return 1
		elif [ $start = "https:/" ]; then
			return 1
		else
			return 0
		fi
	fi
}

if [ $# -lt 2 ];then
	echo 请输入APK文件路径和输入路径
	echo eg: ./auto-apktool.sh abc.apk outdir
	exit -1
fi

is_url $1
isurl=$?

# 如果url，先下載
if [ $isurl -eq 1 ]; then
	path=$2.apk
	curl $1 -o $path

	curl_result=$?

	if [ $curl_result != 0 ];then
		log I 下载apk失败
		exit -5
	fi
else
	if [ ! -f $1 ]; then
		echo apk路径不存在
		exit -4
	fi
	path=$1
fi

# handle resources
if [ ! -f $path ];then
    log I FILE_NOT_FOUND
fi
apktool d $path
log I "Resources disassamble success!"

# unzip apk into output
unzip -q $path -d $2
cd $2

# dex2jar dir
# input your dex2jar full path here
if [[ ! -f $dex2jar ]]; then
	echo 请确定dex2jar路径正确
	exit -3
else
	echo $dex2jar
fi

for dex in `ls *.dex`
do
    echo $dex
    $dex2jar $dex
    echo convert $dex success
done

# input your jd-gui full path here
echo $jdgui
# jd-gui 路径
if [[ ! -f $jdgui ]]; then
	echo 请确定jd-gui路径正确
	exit -2
else
	echo $jdgui
fi

for jar in `ls *.jar`;do
    echo $jar
    $jdgui $jar &
done

