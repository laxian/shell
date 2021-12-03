#!/usr/bin/env bash

find . -name "signed-*-debug*.apk" | xargs -II -n 1 rm I