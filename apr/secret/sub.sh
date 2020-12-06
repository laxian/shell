#!/bin/bash

# sed 替换的简单实用
# $1 oldstr
# $2 newstr
# $3 search dir
# $4 filter fild extension

echo $@

dir=${3:-.}
oldstr=$1
newstr=$2
ext=${4:-*}

if [ -z $4 ]; then
    sed -i s/$oldstr/$newstr/g $(grep $oldstr -rl $dir --exclude-dir private --exclude-dir "*/venv*")
else
    sed -i s/$oldstr/$newstr/g $(grep $oldstr -rl $dir --include "*.$ext" --exclude-dir private --exclude-dir "*/venv*")
fi
