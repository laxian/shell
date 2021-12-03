#!/usr/bin/env bash -x

pushd /Users/leochou/Work
declare -a gradles=`grep nft-sdk -rIl . --include="*.gradle" | grep -vE "(nft-sdk/|nav_app2|cabinet|scooter_app|vision_algo|Kit/)"`
echo -------
for l in `echo $gradles`;do
	echo $l
	sed -i 's/\(.*nft-sdk:\).*\().*\)/\10.0.1.2\"\2/' $l
done
popd
