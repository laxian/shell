#!/usr/bin/env bash

workdir=$(
    cd $(dirname $0)
    pwd
)
echo $workdir
parent=`dirname $workdir`

java -jar $parent/files/signapk.jar $parent/private/rk/platform.x509.pem $parent/private/rk/platform.pk8 $1 $2
