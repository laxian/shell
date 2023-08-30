#!/usr/bin/env bash


mosquitto_pub \
-u EVT7-8 \
-P 3f1a4b2f8686037c \
-t robot/S1RMM2211C0033/log/cmd/send \
-h device-gateway-bj.loomo.com -p 13041 \
--cafile ca_crt \
--cert client_crt \
--key client_key \
--insecure \
-i zwx2 \
-m '{"commandId":1,"commandType":"doRSA","mCmdMessageInner":"pwd"}' \
-d --will-qos 1