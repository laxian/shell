#!/bin/bash

command_exists() {
    command -v "$@" >/dev/null 2>&1
}

if command_exists $1; then
    (
        set -x
        sh -c "type $1"
    )
fi
