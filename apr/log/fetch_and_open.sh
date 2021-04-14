#!/usr/bin/env bash

# ----------------------------
# 快速下载日志
# $1 robot id 关键字过滤
# $2 指定拉取第行，默认0
# ----------------------------

pwd=$( cd "$( dirname "$0"  )" && pwd )
. $pwd/utils.sh
OUTDIR=~/Downloads
OPEN_APP=code

if [ $# -ne 1 ]; then
    cat <<-EOF
		Usage: ./fetch_and_open.sh <url>
	EOF
    exit 1
fi


url=$1
# 获取文件名部分
file_name=${url##*/}
# 获取时间戳部分
timestamp=`echo $file_name | sed 's#.*_\([0-9]\{4\}.*\)-.*#\1#g'`
# id和时间戳拼接作为解压目录
dir=$OUTDIR/${id}-${timestamp}
# 下载为默认名字
download $url
# 解压到指定路径
unzip_to_dir $file_name $dir
# 解压后打开
$OPEN_APP $dir
# 清理本地压缩包
rm $file_name
# 成功提示
echo enjoy!!!

