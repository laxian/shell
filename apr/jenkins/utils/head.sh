#!/usr/bin/env bash

# ---------------------------------------
# http HEAD
# 访问url，只获取header，判断url是否可以访问
# ---------------------------------------

head() {
    status=$(curl -s -m 5 -IL $1 | grep 200 | cut -d' ' -f2)
    if ((status == 200)); then
        return 0
    else
        return 1
    fi
}

# head $1
