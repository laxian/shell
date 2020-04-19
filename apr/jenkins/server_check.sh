#!/usr/bin/env bash

nginx_url_=http://localhost/share/
resty_url_=http://localhost:8082/files/jenkins/
nexus_url_=http://localhost:8081/#browse/browse:rawrepo
maven_url_=http://localhost:8081/#browse/browse:maven-releases

. ./utils/head.sh
head $nexus_url_ && export nginx="[nginx](${nginx_url_})"
head $resty_url_ && export resty="[resty](${resty_url_})"
head $nexus_url_ && export nexus="[nexus](${nexus_url_})"
head $maven_url_ && export maven="[maven](${maven_url_})"

echo $nginx
echo $resty
echo $nexus
echo $maven
