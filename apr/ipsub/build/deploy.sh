#!/usr/bin/env bash

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

sign() {
	name=`basename $1`
	~/Github/shell/apr/demo/sign.sh $1 ./signed-$name
}

commit() {
	pushd $1 && git add . && git commit -m $2 && popd
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
		git stash
		git checkout -b dev
		git pull
		git checkout -b zhouweixian/ip_allin_10

		# 调用外部工具，批量替换http相关、mqtt相关地址
		popd
		pwd
		../mqtt/mqtt.sh ./projs
		commit $l 'MQTT URL UPDATED (AUTO-MODIFIED)'
		../http/http.sh ./projs
		commit $l 'HTTP URL UPDATED (AUTO-MODIFIED)'

		pushd $l
		# 构建、或者跳过构建；签名、复制到根目录
		if [ $skip_build = false ]; then
			rm signed-*-debug.apk
			./gradlew assembleDebug
			[ $? != 0 ] && exit 1
			find . -name "*-debug*.apk" | xargs -I@ bash -c "$(declare -f sign) ; echo @ ; sign @"
		else
			echo skip build
		fi
		
		# 循环批量安装apk
		# adb install -r signed-*-debug.apk
		for f in $(ls signed-*.apk);do
			adb install -r $f
		done
		popd
	else
		echo "--- skip $l, not exists ---"
	fi
done

echo BUILD SUCCESS!

# 复制出来放在同一个目录
echo COPY TO IP DIRECTORY...
./tr_cp.sh S1D
