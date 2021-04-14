#!/bin/bash

darwin=false
linux=false
case "$(uname)" in
Linux*)
    cygwin=true
    ;;
Darwin*)
    darwin=true
    ;;
esac

if [[ $linux == true ]]; then
    ifconfig | grep -E "inet (addr|地址)" | grep -v 127.0.0.1 | awk '{print $2}' | awk -F: '{print $2}' | tail
elif [[ $darwin == true ]]; then
    ipconfig getifaddr en0
else
    echo unknown system
    echo 127.0.0.1
fi
