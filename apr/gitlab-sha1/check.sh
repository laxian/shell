#!/usr/bin/env bash

project=${1:-D2}
branch=${2:-release}

# python mail2.py 'S2_Interaction_Release_' | browser
# python mail2.py 'S1D_release_1.1.73' | browser
# python mail2.py 'GX_Navigation_release_' | browser
# python mail2.py 'D2_release_' | browser

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

# 邮件命名太乱，DEV暂不支持

# if [ $branch == "release" ]; then
# 	branch="release"
# 	repo=$(node rl.js)
# 	mail=$(python3 mail3.py)
# elif [ $branch == "dev" ]; then
# 	branch="dev"
# else
# 	echo not supported, exit
# 	exit 1
# fi

repo=$(node rl.js)
repo2=$(node rl_algo.js)
repo=$repo$repo2
# echo "$repo"
page=$(python3 mail3.py $filter page)
# page=$(cat page)
# echo --------------------------------
# echo "$page"
# echo --------------------------------2
mail=$(cat <<<"$page" | sed -n 's/.*\w.\w.\w\+\.\([0-9a-f]\{7,\}\).*/\1/p' | sort | uniq)
# echo $mail
# echo --------------------------------4

for sha1 in $mail; do
	# echo "================================================$sha1"
	info=$(echo "$page" | sed -nE "/$sha1/s/\s+<li>(\w+):\s+'?(.*)'?<\/li>/\1 \2/p")
	[ -z info ] && info="$sha1"
	if grep -q "$sha1" <<<"$repo"; then
		echo "> [✅] $info"
	else
		echo "> [❌]<font color="error">$info in mail NOT FOUND in latest repo! </font>\n"
	fi
done
