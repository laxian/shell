#!/usr/bin/env bash

grep -E "(http|https)://" -rI . | sed -n 's#.*\(https\{0,1\}:\/\/[a-zA-Z0-9/?&%+-_=/]\+\).*#\1#g;s#,##;s#\]##;p' | sort | uniq