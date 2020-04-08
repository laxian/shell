#!/bin/bash

d2j_version=2.0
jadx_version=1.1.0
apktool_version=2.4.1

tools_dir=env

d2j_url=https://jaist.dl.sourceforge.net/project/dex2jar/dex2jar-$d2j_version.zip
jadx_url=https://bintray.com/skylot/jadx/download_file?file_path=jadx-$jadx_version.zip
apktool_url=https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_$apktool_version.jar

d2j=${d2j_url##*/}
jadx=${jadx_url##*=}
apktool=${apktool_url##*/}

mkdir -p $tools_dir && cd $tools_dir

if [ -e $d2j ]; then
    echo $d2j exists
else
    curl -O $d2j_url
fi

if [ -e $jadx ]; then
    echo $jadx exists
else
    curl -L -o ${jadx_url##*=} $jadx_url
fi

if [ -e $apktool ]; then
    echo $apktool exists
else
    curl -O -L $apktool_url
fi

d2j_dir=${d2j%*.}
jadx_dir=${jadx%*.}
unzip -n $d2j
chmod +x $d2j_dir /*.sh
# test d2j-dex2jar.sh
$d2j_dir/d2j-dex2jar.sh

unzip -n $jadx -d $jadx_dir
chmod +x $jadx_dir/bin/*
# test jadx-gui
jadx_dir/bin/jadx-gui

cat ../jar_wrapper.sh ./$apktool >apktool.sh && chmod +x apktool.sh
# test apktool.sh
./apktool.sh
