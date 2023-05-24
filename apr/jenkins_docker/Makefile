# JENKINS_JOB := app-apr-food-delivery-debug
# JENKINS_JOB := app-restaurant-debug
# JENKINS_JOB := gx-appservice
# JENKINS_JOB := Gx_Service
JENKINS_JOB := nav_app-debug
# JENKINS_JOB := r1_app-debug
# JENKINS_JOB := d2_app-debug
# JENKINS_JOB := module-graph
# JENKINS_JOB := ai_service_app-debug


.PHONY: build clean

sub:
	-../secret/remove_sensitive.sh . sub
res:
	-../secret/remove_sensitive.sh . res

setup: res
	scp -P 2222 -r ../jenkins_docker/* root@${host}:/var/jenkins_home/workspace/$(JENKINS_JOB)
