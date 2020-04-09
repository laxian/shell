#!/bin/bash

subtext=localhost

ip=$(./getip.sh)
echo $ip
sed -i "" s/${ip}/${subtext}/g `grep ${ip} -rl .`
