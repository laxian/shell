#!/usr/bin/env bash -x

IP_APP_DIR=/Volumes/smb_dir/GX_IMG/tmp/ip_app

remove() {
	echo $1 WILL BE REMOVE
	rm $1
}

for sub in `ls` ;do
	dir=$IP_APP_DIR/$sub
	echo $dir
	if [ ! -d $dir ];then
		echo $dir NOT EXISTS
	else	
		for apk in `ls $dir`;do
			if [[ $apk =~ .apk ]]; then
				grep "^$apk$" -rl ./$sub || remove $dir/$apk
			else
				echo $apk NOT apk files, skip
			fi
		done
	fi
done
