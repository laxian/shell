#!/usr/bin/env bash

no_cookie=false
cookie=
if [ -z ./cookie ]; then
    no_cookie=true
else
    cookie=$(cat cookie)
    if [ -z $cookie ]; then
        no_cookie=true
    fi
fi

echo $no_cookie
if [ no_cookie ]; then
    echo ++++++++++++++
    ./login.sh $1 $2
fi

echo ++++++++++++++
./setup_cookie.sh
echo ++++++++++++++
./get_course_list.sh
echo ++++++++++++++
./get_all_course_time.sh course_id_time
echo ++++++++++++++
