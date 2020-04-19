
JENKINS_HOME := /var/jenkins_home
RELATIVE_PATH=workspace/app-apr-food-delivery
CONTAINER := jenkins
PROJECT_ROOT := $(CONTAINER):$(JENKINS_HOME)/$(RELATIVE_PATH)

push: set_ip build remove_ip

build: sign trav wechat_build_finish
	docker cp ./jenkins/jenkins.sh $(PROJECT_ROOT)

sign:
	docker cp ./files/rk/ $(PROJECT_ROOT)
	docker cp ./files/signapk.jar $(PROJECT_ROOT)
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

trav_group: env server_check scan
	docker cp ./jenkins/trav_group.sh $(PROJECT_ROOT)

scan: md_utils
	docker cp ./jenkins/utils/scan.sh $(PROJECT_ROOT)/utils/

wechat_build_finish: env token server_check notify
	docker cp ./jenkins/wechat_build_finish.sh $(PROJECT_ROOT)

token:
	docker cp ./private/token $(PROJECT_ROOT)

notify: md_utils
	docker cp ./jenkins/utils/notify.sh $(PROJECT_ROOT)/utils/

md_utils: 
	docker exec -it jenkins bash -c "[ -d $(JENKINS_HOME)/$(RELATIVE_PATH)/utils ] || mkdir -p $(JENKINS_HOME)/$(RELATIVE_PATH)/utils"

server_check: head
	docker cp ./jenkins/server_check.sh $(PROJECT_ROOT)

head: md_utils
	docker cp ./jenkins/utils/head.sh $(PROJECT_ROOT)/utils/

env:
	docker cp ./jenkins/env.sh $(PROJECT_ROOT)

set_ip:
	./ip/set_ip.sh jenkins

remove_ip:
	./ip/remove_ip.sh jenkins

cd:
	docker exec -it jenkins bash
