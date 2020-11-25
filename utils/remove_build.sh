#!/usr/bin/env bash -x

# ----------------------------
# source remove_build.sh
# rm_build.sh ANDROID_PROJECT_HOME
# 清理android项目各个module目录下的build目录
# ----------------------------

# 指定一个Android项目目录，删除当前目录下的build和子目录下的build
rm_build() {
    echo $1
    for i in $(ls $1); do
        if [[ $i == "build" ]]; then
            echo "rm -rf    $1/$i"
            rm -rf $1/$i
        elif [[ -d $1/$i ]]; then
            for d in $(ls $1/$i); do
                if [[ $d == "build" ]]; then
                    echo "rm -rf    $1/$i/$d"
                    rm -rf $1/$i/$d
                fi
            done            
        fi
    done
}

# 多个Android项目在一个目录下，批量执行
rm_parentdir() {
    for i in $1; do
        rm_build $1
    done
}