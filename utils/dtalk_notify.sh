
#!/bin/bash

# 发送钉钉通知，和Mac桌面通知
# sample：
#   dtalk_notify.sh 买到票了 -d

dingtalk=false
pc=true
name=""
at=""
while [[ $# > 0 ]]; do
    case "$1" in
    -p | --pc)
        echo flag: $1
        pc=true
        shift # shift once since flags have no values
        ;;
    -d | --dingtalk)
        echo flag: $1
        dingtalk=true
        shift # shift once since flags have no values
        ;;
    -a | --at)
        echo flag: $1 $2
        [ dingtalk = 'true' ] && at=$2
        shift 2# shift once since flags have no values
        ;;
    -n | --name)
        echo name $1 with value: $2
        name=$2
        shift 2 # shift twice to bypass switch and its value
        ;;
    *) # unknown flag/switch
        POSITIONAL+=("$1")
        name=$POSITIONAL
        shift
        ;;
    esac
done

set -- "${POSITIONAL[@]}" # restore positional params

function dingtalk_notify() {
    # dingding 抢票消息群webhook url
    curl 'https://oapi.dingtalk.com/robot/send?access_token=71a1ba2bf1be2f47e848c7a28ce981847f817b27dfdf102c0ebd9d2d39056aa4' \
        -H 'Content-Type: application/json' \
        -d '{"msgtype": "text", 
        "text": {
             "content": "'$*'"
        },
        "at": { "atMobiles": [ "18310511388" ], "isAtAll": false }
      }'
}

function pc_notify () {
    osascript -e "display notification \"${strPrompt}\" with title \"$* 完成\""

}


[ $pc = "true" ] && pc_notify $name
[ $dingtalk = "true" ] && dingtalk_notify $name


