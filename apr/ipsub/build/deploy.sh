#!/usr/bin/env bash -x

# -------------------------------------------
# 功能：一键部署IP压缩方案
# 1. 根据projs指定项目目录
# 2. 对每一个项目执行：
# 3. 从最新dev分支创建新分支
# 4. 从ip键值对执行全量搜索替换
# 5. gradle构建
# 6. apk签名并复制到根目录
# 7. apk安装
# 参数：
# 1. 外部传入一个项目路径列表
# 2. 是否跳过构建，适用于已经执行过构建的情况
# -------------------------------------------


APK_DIR=~/Work/IP

workdir=$(
    cd $(dirname $0)
    pwd
)

sign() {
	echo SIGN $1
	name=`basename $1`
	~/Github/shell/apr/demo/sign.sh $1 ./signed-$name
}

commit() {
	pushd $1 && git add . && git commit -m $2; popd
}

namify() {
	echo ==== NAMIFY ====
	for i in $(ls signed-*-debug*.apk); do
		prefix=$(basename $1)
		mv $i "$prefix-$i"
	done
}

archive() {
	dest=$1
	echo COPY TO $dest
	[ ! -d $dest ] && mkdir -p $dest
	ls -l $dest
	cp *-signed-*.apk $dest/
}

list=${1:-projs}
skip_build=${2:-false}
echo $list

OLD_IFS=$IFS
IFS=$'\n'
for l in $(cat $list); do
	if test -d "$l"; then
		# 进入目录，检出dev，pull更新后创建检出到新分支
		pushd $l
		rm *.apk
		git stash
		git checkout s2_lite_dev || git checkout dev2 || git checkout dev-gx || git checkout dev
		git branch --show-current
		git clean -fd
		#git pull
		
		git branch | grep zhouweixian/ip_allin_10 > /dev/null 2>&1
		if [ $? -eq 0 ];then
			git checkout zhouweixian/ip_allin_10
		else
			echo branch EXISTS
			git checkout -b zhouweixian/ip_allin_10
		fi
		#if [ ! $? -eq 0 ];then
		#	echo CREATE GIT BRANCH FAILED!
		#	exit 1
		#fi

		# 调用外部工具，批量替换http相关、mqtt相关地址
		popd
		pwd
		../mqtt/mqtt.sh ./projs
		commit $l 'MQTT URL UPDATED (AUTO-MODIFIED)'

		echo --------------MQTT END----------------

		../http/http.sh ./projs
		commit $l 'HTTP URL UPDATED (AUTO-MODIFIED)'

		echo --------------HTTP END----------------

		pushd $l
		# 构建、或者跳过构建；签名、复制到根目录

		if [ $skip_build = false ]; then
			echo BEGIN GRADLE BUILD
			sed -i '/google/d' build.gradle
			sed -i "/repositories {/a \ \t\tmaven { url 'https://maven.aliyun.com/repository/google' }" build.gradle
			sed -i "/repositories {/a \ \t\tmaven { url 'https://maven.aliyun.com/repository/central' }" build.gradle
			chmod +x ./gradlew
			./gradlew assembleDebug > /dev/null
			[ $? != 0 ] && exit 1
			find . -name "*-debug*.apk" | xargs -I@ bash -c "$(declare -f sign) ; sign @"
		else
			echo skip build
		fi
		
		echo --------------BUILD END----------------

		# 循环批量安装apk
		# adb install -r signed-*-debug.apk
		for f in $(ls signed-*.apk);do
			adb install -r $f
		done

		echo --------------TRY INSTALL END----------------

		namify $l
		echo ==== `pwd` ===
		cat $workdir/kv | grep $l | awk -F: '{print $2}' | tr ',' ' ' | xargs -I@ -n1 bash -c "$(declare -f archive); archive $APK_DIR/@"

		echo --------------ARCHIVE END----------------

		popd
	else
		echo "--- skip $l, not exists ---"
	fi
done
IFS=$'\n'

echo BUILD SUCCESS!

# 复制出来放在同一个目录
echo SYNC TO SMB...
#./sync_smb.sh
