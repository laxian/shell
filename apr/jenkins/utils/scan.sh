#!/usr/bin/env bash

declare -ax apk_array

# 扫描当前目录下以及子目录下的指定类型文件
getdir() {
	echo "--->$1"
	for file in $1/*; do
		if test -f $file; then
			if [ "${file##*.}"x = ${suffix}x ]; then
				echo found ${file}
				# apk_array+="$file "
				len=${#apk_array[*]}
				insert=$((len + 1))
				apk_array[$insert]=$file
			fi
		elif [ -d $file ]; then
			getdir $file
		fi
	done
}

if [ $# -lt 1 ]; then
	cat <<-EOF
		ERROR: wechat_notify need 1 or 2 arguments
		Usage: scan <search_path> [suffix]
		<search_path> path to scan
		[suffix] specify the suffix to scan, defaults to apk.
	EOF
	exit 1
fi

suffix=${2:-apk}
getdir $1
