#!/usr/bin/env bash

project=${1:-D2}
branch=${2:-release}

# python mail2.py 'S2_Interaction_Release_' | browser
# python mail2.py 'S1D_release_1.1.73' | browser
# python mail2.py 'GX_Navigation_release_' | browser
# python mail2.py 'D2_release_' | browser

if [ $branch == 'release' ]; then
	if [ $project = "D2" ]; then
		filter='D2_release_'
	elif [ $project == "S2" ]; then
		filter='S2_Interaction_Release_'
	elif [ $project == "S2NAV" ]; then
		filter='GX_Navigation_release_'
	elif [ $project == "S1" ]; then
		filter='S1D_release_1'
	else
		echo not supported $project, exit
		exit 1
	fi
elif [ $branch == 'dev' ]; then
	# 邮件命名太乱，DEV暂不支持
	if [ $project = "D2" ]; then
		filter='D2_System_Dev_'
	elif [ $project == "S2" ]; then
		filter='Interaction_System_DEV_'
	elif [ $project == "S2NAV" ]; then
		filter='Navigation_System_DEV_'
	elif [ $project == "S1" ]; then
		filter='S1D_System_dev_'
	else
		echo not supported $project, exit
		exit 1
	fi
else
	echo not supported $branch, exit
	exit 1
fi

repo=$(node rl.js $branch)
repo2=$(node rl_algo.js $branch)
repo="$repo $repo2"
# echo "$repo"
page=$(python3 mail3.py $filter page)
# echo "$page">page
# page=$(cat page)
# echo --------------------------------
# echo "$page"
# echo --------------------------------2
mail=$(cat <<<"$page" | sed -n 's/.*\w.\w.\w\+\.\([0-9a-f]\{7,\}\).*/\1/p' | sort | uniq)
# echo $mail
# echo --------------------------------4

for sha1 in $mail; do
	# echo "================================================$sha1"
	info=$(echo "$page" | sed -nE "/$sha1/s/\s+<li>(\w+):\s+'?(.*)'?(<\/li>)?/\1 \2/p")
	[ -z info ] && info="$sha1"
	if grep -q "$sha1" <<<"$repo"; then
		echo "> [✅] $info"
	else
		name=${info% *}
		if [[ $name == "SegwayApp" ]]; then
			name="app-apr-food-deliver"
		fi
		
		repoInfo=$(for n in `echo "$repo"`;do
			echo $n
			done | xargs -n2 | grep "$name")
		echo "> [❌]<font color="error">mail: $info ≠ repo: $repoInfo</font>\n"
	fi
done
