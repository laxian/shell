#!/usr/bin/env bash

# ----------------------------
# 将本地IP目录复制到smb服务器
# ----------------------------

# 如果有一个参数
if [ -n $1 ]; then
	# 如果smb目录已挂载，同步到smb目录
	if [ -d /Volumes/smb_dir/GX_IMG/tmp/ip_app/ ]; then
		echo BEGIN SYNC
		cp /Users/leochou/Work/IP/* /Volumes/smb_dir/GX_IMG/tmp/ip_app/$1
	else
		echo SMB DIR NOT FOUND
	fi
fi

echo SUCCESS