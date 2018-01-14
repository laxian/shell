#!/bin/bash

log() {
	echo -e "LOG_TAG $1:\t$2"
}


# 判斷是否是http地址
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
		log crul 下载apk失败
		exit -5
	fi
else
	if [ ! -f $1 ]; then
		echo apk路径不存在
		exit -4
	fi
	path=$1
fi

# input your jd-gui full path here
jdgui=$JD_HOME/jdgui
echo $jdgui
# jd-gui 路径
if [[ ! -f $jdgui ]]; then
	echo 请确定jd-gui路径正确
	exit -2
else
	echo $jdgui
fi

# dex2jar dir
# input your dex2jar full path here
dex2jar=$D2J_HOME/dex2jar
if [[ ! -f $dex2jar ]]; then
	echo 请确定dex2jar路径正确
	exit -3
else
	echo $dex2jar
fi

# unzip apk into output
unzip -q $path -d $2
cd $2

for dex in `ls *.dex`
do
    echo $dex
    $dex2jar $dex
    echo convert $dex success
done

for jar in `ls *.jar`;do
    echo $jar
    java -jar $jdgui $jar &
done


