#!/usr/bin/env bash -x

# ----------------------------
# 参数1，smb相对路径:D2  S1D S2/
# ----------------------------

namify() {
	for i in $(ls signed-*-debug*.apk); do
		prefix=$(basename $1)
		mv $i "$prefix-$i"
	done
}

for d in $(cat projs); do
	echo $d
	if [ -d $d ]; then
		pushd $d
		# if [ ls signed-*-debug.apk ]; then
		# 	ls signed-*-debug.apk
		# else
		# 	echo not found
		# fi

		ls signed-*-debug*.apk >/dev/null 2>&1 || echo "Not found" && namify $d
		ls *signed-*-debug*.apk >/dev/null 2>&1 && mv *-signed-*-debug*.apk ../IP

		# 如果有一个参数
		if [ -n $1 ]; then
			# 如果smb目录已挂载，同步到smb目录
			if [ -d /Volumes/smb_dir/GX_IMG/tmp/ip_app/ ]; then
				cp ../IP/* /Volumes/smb_dir/GX_IMG/tmp/ip_app/$1
			else
				echo SMB DIR NOT FOUND
			fi
		else
			echo "SMB DIR NOT FOUND"
		fi

		popd
		echo --------------------------------2
	else
		echo $d is not a directory and SKIP
	fi
done