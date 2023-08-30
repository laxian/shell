#!/usr/bin/env bash


mosquitto_sub \
-u EVT7-8 \
-P 3f1a4b2f8686037c \
-t robot/S1RMM2211C0033/log/cmd/send \
-h device-gateway-bj.loomo.com -p 13041 \
--cafile ca_crt \
--cert client_crt \
--key client_key \
--insecure \
-i zwx \ # 不能重复
-d --will-qos 1



mosquitto_sub \
-u GXBOX-EVT8-7 \
-P cf16067e91b90fa14258dc4bb39ed371 \
-t robot/S1RMM2211C0033/log/cmd/command \
-h device-gateway-bj.loomo.com -p 13080 \
--cafile ca_crt \
--cert client_crt \
--key client_key \
--insecure \
-i zwx \
-d --will-qos 1