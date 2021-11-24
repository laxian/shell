#!/usr/bin/env bash

adb shell pm list package | grep segway | awk -F: '{print $2}' | xargs -n 1 -II adb shell pm path I | grep data