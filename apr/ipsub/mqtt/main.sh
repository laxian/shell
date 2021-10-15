#!/usr/bin/env bash

TOOL_PATH=/Users/leochou/Github/shell/apr/secret
export PATH=$TOOL_PATH:$PATH

OLD_IFS=$IFS
IFS=$'\n'
for l in $(cat projs); do
	if [ -d $l ]; then
		cp -R private $l
		echo "--- handling $l ---"
		echo "############### JSON ################"
		remove_sensitive.sh $l sub json

		echo "############### JAVA ################"
		remove_sensitive.sh $l sub java

		echo "############### KT ################"
		remove_sensitive.sh $l sub kt
		rm -rf $l/private

		echo "--- handling $l SUCCESS ---"
	else
		echo "--- skip $l, not exists ---"
	fi
done
IFS=$OLD_IFS
