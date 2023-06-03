JENKINS_JOB := get-release-sha1


.PHONY: build clean

sub:
	-../secret/remove_sensitive.sh . sub
res:
	-../secret/remove_sensitive.sh . res

setup: res
	scp -P 2222 -r ./*.js root@${jenkins_host}:/var/jenkins_home/workspace/$(JENKINS_JOB)
	scp -P 2222 -r ./*.py root@${jenkins_host}:/var/jenkins_home/workspace/$(JENKINS_JOB)
	scp -P 2222 -r ./*.sh root@${jenkins_host}:/var/jenkins_home/workspace/$(JENKINS_JOB)
	scp -P 2222 -r ./private/ root@${jenkins_host}:/var/jenkins_home/workspace/$(JENKINS_JOB)

init:
	npm install

browser:
	node rl.js | xargs -n2 -II echo "I </br>"| browser
	node dev.js | xargs -n2 -II echo "I </br>"| browser

mail:
	python mail2.py 'S2_Interaction_Release_' | browser
	# python mail2.py 'S1D_release_1.1.73' | browser
	# python mail2.py 'GX_Navigation_release_' | browser
	# python mail2.py 'D2_release_' | browser

check:
	./check.sh S2
	./check.sh S2NAV
	./check.sh S1
	./check.sh D2

jenkins:
	./jenkins.sh dev
	./jenkins.sh release
	./jenkins.sh check_s1
	./jenkins.sh check_s2
	./jenkins.sh check_s2nav
	./jenkins.sh check_d2
