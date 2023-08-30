mosquitto_sub \
-u EVT7-8 \
-P 3f1a4b2f8686037c \
-t robot/S1RMM2147C0023/log/cmd/send \
-h ssl://device-gateway-bj.loomo.com -p 13080 \
--cafile ca_crt \
--cert client_crt \
--key client_key \
--insecure \
-i zwx
	
