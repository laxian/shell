# JENKINS_JOB := app-apr-food-delivery-debug
# JENKINS_JOB := app-apr-food-delivery-r1-1
# JENKINS_JOB := gx-appservice
# JENKINS_JOB := Gx_Service
# JENKINS_JOB := nav_app-debug


.PHONY: build clean

sub:
	-../secret/remove_sensitive.sh . sub
res:
	-../secret/remove_sensitive.sh . res

setup: res
	scp -P 2222 -r ../jenkins_docker/* root@10.10.80.25:/var/jenkins_home/workspace/$(JENKINS_JOB)