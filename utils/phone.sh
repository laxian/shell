#!/bin/sh

echo zip $1 into $1.zip
zip -r $1.zip $1
if [ $!=0 ]; then
    echo zip success
else
    echo zip faild, EXIT
    exit
fi

echo begin pushing
adb push $1.zip /sdcard/
echo push success
