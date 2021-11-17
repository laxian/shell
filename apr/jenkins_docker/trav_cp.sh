#!/bin/bash -x

#----------------------------------------------------------------
# jenkins 参数化构建，动态指定分支等参数
#----------------------------------------------------------------

echo ============ begin build ============

workdir=$(
        cd $(dirname $0)
        pwd
)

# 用于在非Jenkins环境使用
[ ! $JENKINS_HOME ] && {
        export ANDROID_HOME=/opt/app/android-sdk
        export JAVA_HOME=/usr/local/openjdk-8
        export PATH=$JAVA_HOME/bin:$PATH
        sign=true
 }

module=${1:-app}
echo $br
echo $variant
echo $sign
echo $module
echo $use_aliyun_maven

VARIANT_ALL="all"
VARIANT_ALPHA="alpha"
VARIANT_DEBUG="debug"
VARIANT_RELEASE="release"

# 切换到参数指定分支
[ -n "$br" ] && git checkout -f $br && git reset --hard HEAD
#WORKSPACE=.
JENKINS_HOME=/var/jenkins_home
GIT_REV=$(git rev-parse --short HEAD)
#GIT_BRANCH=`git branch --show-current`
GIT_BRANCH=$(git name-rev --name-only HEAD)
echo $GIT_BRANCH
echo $GIT_REV
COMMIT=$(git log -n 1 | sed '/\(commit\|Author\|Date\|Merge:\|Merge branch\|See merge\|^[ ]*$\)/d' | tr -d ' ')

# gradle执行前的一些操作，如果有，加在这里
. ./before_build.sh

# 开始构建
$workdir/gradlew clean
if [ $variant == $VARIANT_RELEASE ]; then
        $workdir/gradlew :$module:assembleRelease
elif [ $variant == $VARIANT_ALPHA ]; then
        $workdir/gradlew :$module:assembleAlpha
elif [ $variant == $VARIANT_DEBUG ]; then
        $workdir/gradlew :$module:assembleDebug
else
        $workdir/gradlew build
fi

. $workdir/utils/notify.sh
# gradle失败后直接报错退出
if [ $? != 0 ]; then
        err_msg="构建失败: $GIT_BRANCH - ${BUILD_URL}console"
        wechat_notify $token $err_msg
        exit 1
fi

time=$(date "+%Y-%m-%d_%H_%M_%S")
# apkdir=app/build/outputs/apk/
apkdir=.
outdir=$JENKINS_HOME/outputs/$time
mkdir -p $outdir
host="10.10.80.25:8080"
url=http://$host/files/$time

# 复制apk到指定目录，outdir和tomcat托管目录磁盘映射
find $apkdir -name "*.apk" | xargs -I F cp F $outdir

# 签名
if [ $sign == 'true' ]; then
        pushd $outdir
        for apk in $(ls $outdir/*.apk); do
                # 如果不带git hash，加上
                if [ ! `echo $apk | grep $GIT_REV` ]; then
                        apk_old=$apk
                        apk="${apk//.apk/}-$GIT_REV.apk"
                        mv $apk_old $apk
                        unset apk_old
                fi
                # 如果带unsigned，去掉
                mv $apk ${apk//-unsigned/}
                $workdir/sign.sh $apk "${apk//.apk/}-signed.apk"
        done
        popd
fi

# 微信通知
token=$(cat ./private/token)
urls="apks:\n$JOB_NAME\n$GIT_BRANCH\n$GIT_REV\n$COMMIT\n"
for f in $(ls $outdir); do
        uri=$url/$f
        block="[$f]($uri)"
        urls="$urls\n$block"
done
echo $urls
wechat_notify $token $urls
