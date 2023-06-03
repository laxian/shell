#!/usr/bin/env bash

# 用于在非Jenkins环境使用
[ ! $JENKINS_HOME ] && {
	echo running in terminal
	br=${1:-release}
} || {
	echo running in Jenkins
	pwd
	ls
	env
}

#  [ -n "$gitlabBranch" ] branch

[[ -d node_modules ]] || npm install node-fetch
[ $br == 'dev' ] && resp=$(node dev.js) || resp=$(node rl.js)

if [ $br == 'dev' ]; then
	resp=$(node rl.js dev)
	resp2=$(node rl_algo.js dev)
	resp="$resp\n$resp2"
elif [ $br == 'release' ]; then
	resp=$(node rl.js)
	resp2=$(node rl_algo.js)
	resp="$resp\n$resp2"
elif [ $br == 'nav_dev' ]; then
	resp=$(node rl_algo.js dev)
elif [ $br == 'nav_release' ]; then
	resp=$(node rl_algo.js)
elif [ $br == 'check_d2' ]; then
	resp=$(./check.sh D2)
elif [ $br == 'check_s2' ]; then
	resp=$(./check.sh S2)
elif [ $br == 'check_s2nav' ]; then
	resp=$(./check.sh S1)
elif [ $br == 'check_s1' ]; then
	resp=$(./check.sh S1)
elif [ $br == 'check_d2_dev' ]; then
	resp=$(./check.sh D2 dev)
elif [ $br == 'check_s2_dev' ]; then
	resp=$(./check.sh S2 dev)
elif [ $br == 'check_s2nav_dev' ]; then
	resp=$(./check.sh S1 dev)
elif [ $br == 'check_s1_dev' ]; then
	resp=$(./check.sh S1 dev)
else
	exit
fi

token=$(cat private/token | head -n1)
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

echo "$resp"
wechat_notify $token "$br:\n$resp"
