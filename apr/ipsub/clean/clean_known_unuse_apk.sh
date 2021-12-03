#!/usr/bin/env bash -x

pushd /Users/leochou/Work/IP
find . -name "*live*.apk" | xarg rm
find . -name "*tabletmonitor*.apk" | xargs rm
find . -name "*signed.apk" | xargs rm
find /Volumes/smb_dir/GX_IMG/tmp/ip_app/ -name "*signed*signed*.apk" | xargs rm
popd
