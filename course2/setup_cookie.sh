#!/usr/bin/env bash

#----------------------------------------------------------------
# 设置cookie工具，将代码里含有'YOUR_COOKIE'字段的文件里的此字段替换为真实cookie
#----------------------------------------------------------------

cookie=$(cat cookie)
if [ -z "$cookie" ]; then
    echo "请输入cookie"
    exit 1
else
    echo $cookie
fi

setCookie() {
    f=$1
    sed -i "s#YOUR_COOKIE#$cookie#g" $f
}

for f in $(grep YOUR_COOKIE -rl .); do
    if [ $f != $0 ]; then
        echo $f --------
        setCookie $f
    fi
done
