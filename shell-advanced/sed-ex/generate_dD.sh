#!/usr/bin/env bash -x

#---------------------------------------
# 生成n行，第x行后跟随x行空行
#---------------------------------------


function append() {
	for i in `seq $1`;do
		echo "" >> $2
	done
}


for i in `seq 15`; do
	echo this is the $i line >> dD
	append $i dD
done


