
.PHONY: build clean

sub:
	-../secret/remove_sensitive.sh . sub
res:
	-../secret/remove_sensitive.sh . res

setup: res
	scp -P 2222 -r ../jenkins_docker/ root@${host}:/var/jenkins_home/workspace/app-apr-food-delivery-debug