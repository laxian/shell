#!/usr/bin/env bash

workdir=$(
    cd $(dirname $0)
    pwd
)

java -jar $workdir/../files/signapk.jar $/workdir/../private/rk/platform.x509.pem $workdir/../private/rk/platform.pk8 $1 $2
