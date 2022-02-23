#!/usr/bin/env bash -x

workdir=$(
    cd $(dirname $0)
    pwd
)

apply_aar() {
	echo $1
	dir=`dirname $1`
	echo CREATE LIBS DIR
	libs=$dir/libs
	mkdir -p $libs
	echo COPY AAR TO $libs
	cp ./nft-sdk/nft-sdk/build/outputs/aar/nft-sdk.aar $libs
	echo ADD DIR TO MAVEN
	sed -i '/dependencies {/irepositories{\nflatDir { dirs '\''libs'\''  }\n}' $1
	echo remove maveqn-implementation ADD AAR-implementation
	sed -i "/nft-sdk/d" $1
	sed -i "/dependencies/a \    implementation name: 'nft-sdk', ext: 'aar'" $1
	echo DONE!!!
}

pushd /Users/leochou/Work/
declare -a gradles=`grep nft-sdk -rIl . --include="*.gradle" | grep -vE "(nft-sdk/|nav_app2|cabinet|scooter_app|vision_algo|Kit/)"`
for l in `echo $gradles`;do
	echo $l
	[ $l = "./GxSystemDevKit2/debuglogservice/build.gradle" ] && apply_aar $l
done
popd

