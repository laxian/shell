
dingtalk=false
pc=false
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
        shift
        ;;
    esac
done

set -- "${POSITIONAL[@]}" # restore positional params

function dingtalk_notify() {
    curl 'https://oapi.dingtalk.com/robot/send?access_token=xxx' \
        -H 'Content-Type: application/json' \
        -d "{ \"msgtype\": \"text\", \"text\": { \"content\": \"您的任务已完成: $1\" }, \"at\": { \"atMobiles\": [ \"18310511388\" ], \"isAtAll\": false } }"
}

function pc_notify () {
    osascript -e "display notification \"${strPrompt}\" with title \"$1 完成\""

}


[ $pc = "true" ] && pc_notify $name
[ $dingtalk = "true" ] && dingtalk_notify $name


