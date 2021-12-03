#!/usr/bin/env bash -x

IP_APP_DIR=/Volumes/smb_dir/GX_IMG/tmp/ip_app

for sub in `ls $IP_APP_DIR`;do
	dir=$IP_APP_DIR/$sub
	ls $dir > $sub
	echo $sub-2
done

