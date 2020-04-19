#!/usr/bin/env bash

nginx_url_=http://localhost/share/
resty_url_=http://localhost:8082/files/jenkins/
nexus_url_=http://localhost:8081/#browse/browse:rawrepo
maven_url_=http://localhost:8081/#browse/browse:maven-releases

nginx_status=$(curl -s -m 5 -IL $nginx_url_ | grep 200 | cut -d' ' -f2)
resty_status=$(curl -s -m 5 -IL $resty_url_ | grep 200 | cut -d' ' -f2)
nexus_status=$(curl -s -m 5 -IL $nexus_url_ | grep 200 | cut -d' ' -f2)
maven_status=$(curl -s -m 5 -IL $maven_url_ | grep 200 | cut -d' ' -f2)

[[ "$nginx_status" == 200 ]] && export nginx="[nginx](${nginx_url_})"
[[ "$resty_status" == 200 ]] && export resty="[resty](${resty_url_})"
[[ "$nexus_status" == 200 ]] && export nexus="[nexus](${nexus_url_})"
[[ "$maven_status" == 200 ]] && export maven="[maven](${maven_url_})"

echo $nginx
echo $resty
echo $nexus
echo $maven
