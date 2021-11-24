#!/usr/bin/env bash

# -------------------------------------------
# 一键部署IP压缩方案
# 1. 根据projs指定项目目录
# 2. 对每一个项目执行：
# 3. 从最新dev分支创建新分支
# 4. 从ip键值对执行全量搜索替换
# 5. gradle构建
# 6. apk签名并复制到根目录
# 7. apk安装
# -------------------------------------------


APK_DIR=~/Work/IP

sign() {
	name=`basename $1`
	~/Github/shell/apr/demo/sign.sh $1 ./signed-$name
}

list=${1:-projs}
skip_build=${2:-false}
echo $list

OLD_IFS=$IFS
IFS=$'\n'
for l in $(cat $list); do
	if test -d "$l"; then
		pushd $l
		rm signed-*-debug.apk
		git stash
		git checkout -b dev
		git pull
		git checkout -b zhouweixian/ip_allin_10

		popd
		../http/http.sh ./projs
		../mqtt/http.sh ./projs
		pushd $l

		if [ $skip_build = false ]; then
			./gradlew assembleDebug
			find . -name "*-debug.apk" | xargs -I@ bash -c "$(declare -f sign) ; echo @ ; sign @"
		else
			echo skip build
		fi
		
		# adb install -r signed-*-debug.apk
		for f in $(ls signed-*.apk);do
			adb install -r $f
		done

	else
		echo "--- skip $l, not exists ---"
	fi
done