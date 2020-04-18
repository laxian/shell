#!/usr/bin/env bash

java -jar signapk.jar ./rk/platform.x509.pem ./rk/platform.pk8 app/build/outputs/apk/alpha/segway-delivery-alpha.apk app/build/outputs/apk/alpha/segway-delivery-alpha-signed.apk
