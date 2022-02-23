mosquitto_sub \
-u ${name} \
-P ${password} \
 -t robot/${name}/log/cmd/send \
 -h ${ip} -p 8884 \
 --cafile ca_crt \
 --cert client_crt \
 --key client_key  \
 --insecure \
 -d
