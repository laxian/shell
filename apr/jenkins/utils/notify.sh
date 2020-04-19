#!/usr/bin/env bash

# wechat_notify token content
wechat_notify() {

	if [ $# -lt 2 ]; then
		cat <<-EOF
			ERROR: wechat_notify need exactly 2 arguments
			Usage: wechat_notify token content
		EOF
		exit 1
	fi

	token=$1
	content="$2"
	notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token
	json="{
		\"msgtype\": \"markdown\",
		\"markdown\": {
			\"content\": \"$content\"
		}
   }"

	echo $json

	curl $notify_url \
		-H 'Content-Type: application/json' \
		-d "$json"
}
