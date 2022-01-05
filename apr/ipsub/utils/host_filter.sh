#!/usr/bin/env bash

grep -E "(http|https)://" -rI . | sed -n 's#.*\(https\?:\/\/[a-zA-Z0-9\.-]\+\).*#\1#;s#,##;s#\]##;p'