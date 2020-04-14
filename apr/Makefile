
PROJECT_ROOT := jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

push: set_ip token env trav_cp trav_send trav_nexus trav_maven trav_group wechat_build_finish remove_ip

wechat_build_finish: 
	docker cp ./jenkins/wechat_build_finish.sh $(PROJECT_ROOT)

token:
	docker cp ./jenkins/token $(PROJECT_ROOT)

env:
	docker cp ./jenkins/env.sh $(PROJECT_ROOT)

trav_cp:
	docker cp ./jenkins/trav_cp.sh $(PROJECT_ROOT)

trav_send:
	docker cp ./jenkins/trav_send.sh $(PROJECT_ROOT)

trav_nexus:
	docker cp ./jenkins/trav_nexus.sh $(PROJECT_ROOT)

trav_maven:
	docker cp ./jenkins/trav_maven.sh $(PROJECT_ROOT)

trav_group:
	docker cp ./jenkins/trav_group.sh $(PROJECT_ROOT)

set_ip:
	./ip/set_ip.sh jenkins

remove_ip:
	./ip/remove_ip.sh jenkins

cd:
	docker exec -it jenkins bash
