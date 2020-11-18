#!/bin/zsh
echo 给我截图！
time=$(date +%H%M%s)
adb shell screencap -p sdcard/${time}.png
adb pull sdcard/${time}.png