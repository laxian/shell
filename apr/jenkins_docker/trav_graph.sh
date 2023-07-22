#!/bin/bash -x

#----------------------------------------------------------------
# jenkins 参数化构建，动态指定分支等参数
# 支持gitlab触发构建：
# https://plugins.jenkins.io/gitlab-plugin/     
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

# 切换到参数指定分支
[ -n "$br" ] && git checkout -f $br && git reset --hard origin/$br
# gitlabBranch 是gitlab触发的构建内置的环境变量，和br不同时存在
[ -n "$gitlabBranch" ] && git checkout -f $gitlabBranch && git reset --hard origin/$gitlabBranch
#WORKSPACE=.
JENKINS_HOME=/var/jenkins_home
GIT_REV=$(git rev-parse --short HEAD)
#GIT_BRANCH=`git branch --show-current`
GIT_BRANCH=$(git name-rev --name-only HEAD)
echo $GIT_BRANCH
echo $GIT_REV

# gradle执行前的一些操作，如果有，加在这里
. ./before_build.sh

if [ task = "graph" ]; then
        ./graph.sh
else
        VARIANT_ALL="all"
        VARIANT_ALPHA="alpha"
        VARIANT_DEBUG="debug"
        VARIANT_RELEASE="release"

        # 开始构建
        # $workdir/gradlew clean
        if [ $variant == $VARIANT_RELEASE ]; then
                $workdir/gradlew :$module:assembleRelease 2> error
        elif [ $variant == $VARIANT_ALPHA ]; then
                $workdir/gradlew :$module:assembleAlpha 2> error
        elif [ $variant == $VARIANT_DEBUG ]; then
                $workdir/gradlew :$module:assembleDebug 2> error
        else
                $workdir/gradlew build -xlint 2> error
        fi

        build_result=$?

        tokens=$(cat ./private/token)
        . $workdir/utils/notify.sh
        # gradle失败后直接报错退出
        if [ $build_result != 0 ]; then
                err_msg="$JOB_NAME 构建失败:\n$GIT_BRANCH\n${BUILD_URL}console"
                set
                if [[ -n $gitlabActionType ]]; then
                        err_msg="$err_msg\n$gitlabActionType by $gitlabUserName"
                fi
                if [[ -f error ]]; then
                        error_content=`sed -n '/What went wrong/{N;p;q}' error`
                        err_msg="$err_msg\n$error_content"
                        rm error
                fi
                
                
                for token in $tokens; do
                        wechat_notify $token "$err_msg"
                done
                exit 1
        fi
fi


time=$(date "+%Y-%m-%d_%H_%M_%S")
# apkdir=app/build/outputs/apk/
apkdir=.
outdir=$JENKINS_HOME/outputs/$time
mkdir -p $outdir
host="${host}:8080"
url=http://$host/files/$time

# 复制apk到指定目录，outdir和tomcat托管目录磁盘映射
find $apkdir -name "*.apk" | xargs -I F cp F $outdir

# 签名
if [ $sign == 'true' ]; then
        pushd $outdir
        for apk in $(ls $outdir/*.apk); do
                # 如果不带git hash，加上
                if [ ! $(echo $apk | grep $GIT_REV) ]; then
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

# 显示最近3条git提交log
COMMIT=$(git log --no-merges -n 3 | sed '/\(commit\|Author\|Date\|Merge:\|Merge branch\|See merge\|^[ ]*$\)/d' | tr -d ' ' | sed -n '=;p' | sed -n '{N;s/\n/. /;p;d}')

# 微信通知
urls="apks:\n$JOB_NAME\n$GIT_BRANCH\n$GIT_REV\n$COMMIT\n"
for f in $(ls $outdir); do
        uri=$url/$f
        block="[$f]($uri)"
        urls="$urls\n$block"
done
echo $urls

for token in $tokens; do
        wechat_notify $token "$urls"
done
