#!/bin/bash

./sign.sh
./trav_group.sh app/build/outputs/apk/ /share/$timestamp-$version-$env-$git_version/
./wechat_build_finish.sh
