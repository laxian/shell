

push: set_ip token env trav_cp trav_send trav_nexus trav_group wechat_build_finish remove_ip

wechat_build_finish: 
	docker cp ./jenkins/wechat_build_finish.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

token:
	docker cp ./jenkins/token jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

env:
	docker cp ./jenkins/env.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_cp:
	docker cp ./jenkins/trav_cp.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_send:
	docker cp ./jenkins/trav_send.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_nexus:
	docker cp ./jenkins/trav_nexus.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_group:
	docker cp ./jenkins/trav_group.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

set_ip:
	./ip/set_ip.sh

remove_ip:
	./ip/remove_ip.sh