#!/usr/bin/env bash

for f in `cat projs`;do
	pushd $f
	git log -n 2 | grep AUTO
	echo $f
	popd
	echo --------
done
