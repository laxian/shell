
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
    curl 'https://oapi.dingtalk.com/robot/send?access_token=d7fb2719a1655eb9e067dd549a86385cc7f57e14a056fe52187da85c1adf3159' \
        -H 'Content-Type: application/json' \
        -d "{ \"msgtype\": \"text\", \"text\": { \"content\": \"您的任务已完成: $*\" }, \"at\": { \"atMobiles\": [ \"18310511388\" ], \"isAtAll\": false } }"
}

function pc_notify () {
    osascript -e "display notification \"${strPrompt}\" with title \"$* 完成\""

}


[ $pc = "true" ] && pc_notify $name
[ $dingtalk = "true" ] && dingtalk_notify $name


