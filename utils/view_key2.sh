#!/usr/bin/env bash

# ----------------------------
# print apk certificate
# keytool -printcert -jarfile XXX.apk
# ----------------------------

keytool -printcert -jarfile $1