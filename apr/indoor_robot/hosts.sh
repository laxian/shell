#!/bin/bash

# 获取当前目录下所有host

hosts() {
	grep -E "(http|https)://" -rI . | sed -n 's#.*\(https\?:\/\/[a-zA-Z0-9\.-]\+\).*#\1#;s#,##;s#\]##;p' | sort | uniq
}
