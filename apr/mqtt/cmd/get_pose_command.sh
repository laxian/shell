#!/usr/bin/env bash

# This script is used to get the pose of the robot

function pos_of_num () {
	echo `sed -n "$1 p" private/pos|cut -d',' -f2`
}

function cmd_of_num () {
	echo "input tap "$(pos_of_num $1)
}

function cmds () {
	string=$1
	ret=""
	for (( i=0; i<${#string}; i++ )); do
		cmd=`cmd_of_num ${string:$i:1}`
		if [[ -z $ret ]]; then
			ret="${cmd}"
		else
			ret="${ret};${cmd}"
		fi
		unset cmd
	done
	echo "$ret" 2>&1
	return 0
}

cmds $1