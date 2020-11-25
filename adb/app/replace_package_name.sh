#!/usr/bin/env bash

sed -i "s/<package_name>/$(cat ./private/package_name)/g" Makefile
sed -i "s/<path_to_activity>/$(cat ./private/path_to_activity)/g" Makefile