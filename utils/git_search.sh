#!/usr/bin/env bash

# search in git history for a string
function git_search() {
	if [ $# -ne 1 ]; then
		echo "Usage: git_search \"string\""
		return 1
	fi
	str=$1
	# git rev-list --all | xargs git grep "$str"
	git grep "$str" $(git rev-list --all)
}

git_search $1