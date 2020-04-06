#!/bin/bash

subtext=localhost

ip=$(./getip.sh)
echo $ip
sed -i "" s/${subtext}/${ip}/g `grep ${subtext} -rl .`
