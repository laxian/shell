#!/usr/bin/env bash

sed -i 's/\([^#]*[[:space:]]*\)print[[:space:]]\(.*\)/\1print(\2)/' `find . -name "*.py"`
