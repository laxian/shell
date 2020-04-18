
JENKINS_HOME := /var/jenkins_home

PROJECT_ROOT := jenkins:$(JENKINS_HOME)/workspace/app-apr-food-delivery/

push: build

build: sign trav wechat_build_finish
	docker cp ./jenkins/jenkins.sh $(PROJECT_ROOT)

sign:
	docker cp ./cert/rk/ $(PROJECT_ROOT)
	docker cp ./utils/signapk.jar $(PROJECT_ROOT)
	docker cp ./jenkins/sign.sh $(PROJECT_ROOT)

trav: trav_cp trav_send trav_nexus trav_maven trav_group 

trav_cp:
	docker cp ./jenkins/trav_cp.sh $(PROJECT_ROOT)

trav_send: env
	docker cp ./jenkins/trav_send.sh $(PROJECT_ROOT)

trav_nexus: env
	docker cp ./jenkins/trav_nexus.sh $(PROJECT_ROOT)

trav_maven: env
	docker cp ./jenkins/trav_maven.sh $(PROJECT_ROOT)

trav_group: env server_check
	docker cp ./jenkins/trav_group.sh $(PROJECT_ROOT)

wechat_build_finish: env token server_check notify
	docker cp ./jenkins/wechat_build_finish.sh $(PROJECT_ROOT)

token:
	docker cp ./jenkins/token $(PROJECT_ROOT)

notify: 
	docker cp ./jenkins/notify.sh $(PROJECT_ROOT)

server_check: 
	docker cp ./jenkins/server_check.sh $(PROJECT_ROOT)

env:
	docker cp ./jenkins/env.sh $(PROJECT_ROOT)

set_ip:
	./ip/set_ip.sh jenkins

remove_ip:
	./ip/remove_ip.sh jenkins

cd:
	docker exec -it jenkins bash
