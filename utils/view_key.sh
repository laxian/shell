#!/bin/bash

if [ -z keytool ]; then
	cat <<-EOF
		Error! keytool not found.
		Usage: bash view_key.sh <path_to_apk>.
	EOF
	exit 1
fi

pushd

# 指定解压文件
unzip $1 META-INF/CERT.RSA -d tmp
pushd tmp/META-INF
keytool -printcert -file CERT.RSA
popd

rm -rf tmp/
