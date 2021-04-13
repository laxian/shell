JENKINS_JOB := app-apr-food-delivery-debug
# JENKINS_JOB := gx-appservice
# JENKINS_JOB := Gx_Service


.PHONY: build clean

sub:
	-../secret/remove_sensitive.sh . sub
res:
	-../secret/remove_sensitive.sh . res

setup: res
	scp -P 2222 -r ../jenkins_docker/* root@10.10.80.25:/var/jenkins_home/workspace/$(JENKINS_JOB)