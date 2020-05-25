#!/usr/bin/env bash

ip=$(adb -d shell ifconfig 2>/dev/null | grep "inet addr" | grep -v 127 | awk '{print $2}' | cut -d':' -f2)
[ -z "$ip" ] && ip=$(adb -d shell netcfg 2>/dev/null | grep wlan0 | awk '{print $3}' | cut -d'/' -f1)

echo $ip | awk '{print $1}'
