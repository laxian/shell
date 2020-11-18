#!/usr/bin/env bash

no_cookie=false
cookie=
if [ -z cookie ]; then
    no_cookie=true
elif [[]]; then
    cookie=$(cat cookie)
    if [ -z $cookie ]; then
        no_cookie=true
    fi
fi

if [ no_cookie ]; then
    ./login.sh
fi

./setup_cookie.sh
./get_course_list.sh
./get_all_course_time.sh
