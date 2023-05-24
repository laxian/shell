#!/usr/bin/env bash

workdir=$(
    cd $(dirname $0)
    pwd
)
echo $workdir
java -version
java -jar $workdir/files/signapk.jar $workdir/rl/platform.x509.pem $workdir/rl/platform.pk8 $1 $2
