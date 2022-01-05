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
	name=$(basename $1)
	~/Github/shell/apr/demo/sign.sh $1 ./signed-$name
}

commit() {
	pushd $1 && git add . && git commit -m $2
	popd
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
	pushd $l
	echo --------------ARCHIVE BEGIN----------------
	echo ==== $(pwd) ===
	cat $workdir/kv | grep $l | awk -F: '{print $2}' | tr ',' ' ' | xargs -I@ -n1 bash -c "$(declare -f archive); archive $APK_DIR/@"

	echo --------------ARCHIVE END----------------
	popd
done

IFS=$'\n'

echo BUILD SUCCESS!

# 复制出来放在同一个目录
echo SYNC TO SMB...
./sync_smb.sh
