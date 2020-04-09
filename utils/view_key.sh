#!/bin/bash

unzip $1 -d tmp
cd tmp/META-INF
keytool -printcert -file CERT.RSA
