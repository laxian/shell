

push: setip wtoken trav_cp trav_send trav_nexus trav_group notify

notify: 
	docker cp wechat_build_finish.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

wtoken:
	docker cp token jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_cp:
	docker cp trav_cp.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_send:
	docker cp trav_send.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_nexus:
	docker cp trav_nexus.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

trav_group:
	docker cp trav_group.sh jenkins:/var/jenkins_home/workspace/app-apr-food-delivery/

setip:
	./setip.sh

remove_ip:
	sed -i "" s/192.168.1.68/localhost/g `grep "192.168.1.68" -rl ./apr`

setip:
	./setip.sh