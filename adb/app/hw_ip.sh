#!/usr/bin/env bash

ip=$(./phone_ip.sh)

echo $ip

if [ "$(uname)" != "Darwin" ]; then
    open http://"$ip":8088
else
    python -mwebbrowser http://"$ip":8088
fi
