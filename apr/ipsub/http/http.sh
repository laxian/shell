#!/usr/bin/env bash -x

TOOL_PATH=/Users/leochou/Github/shell/apr/secret
export PATH=$TOOL_PATH:$PATH

workdir=$(
    cd $(dirname $0)
    pwd
)

list=${1:-projs}
echo $list
cat $list

OLD_IFS=$IFS
IFS=$'\n'
for l in $(cat $list); do
	if test -d "$l"; then
		cp -R $workdir/private $l
		echo "--- handling $l ---"
		echo "############### JSON ################"
		remove_sensitive.sh $l sub json

		echo "############### JAVA ################"
		remove_sensitive.sh $l sub java

		echo "############### JAVA ################"
		remove_sensitive.sh $l sub gradle

		echo "############### KT ################"
		remove_sensitive.sh $l sub kt
		rm -rf $l/private

		echo "--- handling $l SUCCESS ---"
	else
		echo "--- skip $l, not exists ---"
	fi
done
IFS=$'\n'
