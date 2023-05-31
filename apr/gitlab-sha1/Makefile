JENKINS_JOB := get-release-sha1


.PHONY: build clean

sub:
	-../secret/remove_sensitive.sh . sub
res:
	-../secret/remove_sensitive.sh . res

setup: res
	scp -P 2222 -r ./rl.js root@${host}:/var/jenkins_home/workspace/$(JENKINS_JOB)
	scp -P 2222 -r ./dev.js root@${host}:/var/jenkins_home/workspace/$(JENKINS_JOB)

init:
	npm install

browser:
	node rl.js | xargs -n2 -II echo "I </br>"| browser
	node dev.js | xargs -n2 -II echo "I </br>"| browser

mail:
	python mail2.py 'S2_Interaction_Release_' | browser
