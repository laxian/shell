#!/usr/bin/env bash -x


pushd /Users/leochou/Work

javas=$(grep -E "http://[a-zA-Z]" -rI . --include="*.java" | grep -vE "(apache|android|google|eclipse|\*|TtsDemo|nav_app2|vision_algo|deliver2|app-apr-food-deliver/|cabinet|GXMonitor/|GxSystemDevKit/|String.format|// |//private|ikoula|lite_app|scooter_app|ExpressActivity)" | sed 's;\(.*java\).*http://\(.*\);\1;' | sort | uniq)
echo $javas
for l in `echo $javas`;do
	echo "$l"
	sed -i 's#http://d#https://d#;s#http://o#https://o#' $l
done

popd
