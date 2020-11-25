#!/bin/bash

script_name=`basename $BASH_SOURCE`

isMain() {
    invoke_name=$(basename $0)
    if [ $invoke_name = $script_name ]; then
        return 0
    else
        return 1
    fi
}

getTimezone() {
    ls -l /etc/localtime | awk -F'zoneinfo/' '{print $2}'
}

if isMain; then
    getTimezone
fi
