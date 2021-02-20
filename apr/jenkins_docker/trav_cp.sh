#!/bin/bash -x

#----------------------------------------------------------------
# jenkins 参数化构建，动态指定分支等参数
#----------------------------------------------------------------

echo ============ begin build ============

workdir=$(
        cd $(dirname $0)
        pwd
)

echo $br
echo $variant
echo $sign

VARIANT_ALL="all"
VARIANT_ALPHA="alpha"
VARIANT_DEBUG="debug"
VARIANT_RELEASE="release"

# 切换到参数指定分支
[ -n "$br" ] && git checkout $br
#WORKSPACE=.
JENKINS_HOME=/var/jenkins_home
GIT_REV=$(git rev-parse --short HEAD)
#GIT_BRANCH=`git branch --show-current`
GIT_BRANCH=$(git name-rev --name-only HEAD)
echo $GIT_BRANCH
echo $GIT_REV
COMMIT=$(git log -n 1 | sed '/\(commit\|Author\|Date\|Merge:\|Merge branch\|See merge\|^[ ]*$\)/d' | tr -d ' ')

# 开始构建
$workdir/gradlew clean
if [ $variant == $VARIANT_RELEASE ]; then
        $workdir/gradlew assembleRelease
elif [ $variant == $VARIANT_ALPHA ]; then
        $workdir/gradlew assembleAlpha
elif [ $variant == $VARIANT_DEBUG ]; then
        $workdir/gradlew assembleDebug
else
        $workdir/gradlew build
fi

time=$(date "+%Y-%m-%d_%H_%M_%S")
# apkdir=app/build/outputs/apk/
apkdir=.
outdir=$JENKINS_HOME/outputs/$time
mkdir -p $outdir
host="${host}"
url=http://$host/files/$time

# 复制apk到指定目录，outdir和tomcat托管目录磁盘映射
find $apkdir -name "*.apk" | xargs -I F cp F $outdir

# 签名
if [ $sign == 'true' ]; then
        pushd $outdir
        for apk in $(ls $outdir/*.apk); do
                new_apk="${apk//.apk/}-$GIT_REV.apk"
                mv $apk $new_apk
                $workdir/sign.sh $new_apk "${new_apk//.apk/}-signed.apk"
        done
        popd
fi

# 微信通知
token=`cat ./private/token`
. $workdir/utils/notify.sh
urls="apks:\n$GIT_BRANCH\n$GIT_REV\n$COMMIT\n"
for f in $(ls $outdir); do
        uri=$url/$f
        block="[$f]($uri)"
        urls="$urls\n$block"
done
echo $urls
wechat_notify $token $urls
