#!/bin/bash -ex

export env=alpha
export timestamp=$(date "+%Y%m%d%H%M%S")
export git_version=`git rev-parse --short HEAD`
export versionCode=`git rev-list HEAD --first-parent --count`
export version=3.0.$versionCode
export server_host=localhost