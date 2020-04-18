#!/usr/bin/env bash

nginx_url=http://localhost/share/
resty_url=http://localhost:8082/files/jenkins/
nexus_url=http://localhost:8081/#browse/browse:rawrepo
maven_url=http://localhost:8081/#browse/browse:maven-releases

nginx_status=$(curl -s -m 5 -IL $nginx_url | grep 200 | cut -d' ' -f2)
resty_status=$(curl -s -m 5 -IL $resty_url | grep 200 | cut -d' ' -f2)
nexus_status=$(curl -s -m 5 -IL $nexus_url | grep 200 | cut -d' ' -f2)
maven_status=$(curl -s -m 5 -IL $maven_url | grep 200 | cut -d' ' -f2)

[[ "$nginx_status" == 200 ]] && export nginx="[nginx](${nginx_url})"
[[ "$resty_status" == 200 ]] && export resty="[resty](${resty_url})"
[[ "$nexus_status" == 200 ]] && export nexus="[nexus](${nexus_url})"
[[ "$maven_status" == 200 ]] && export maven="[maven](${maven_url})"

echo $nginx
echo $resty
echo $nexus
echo $maven
