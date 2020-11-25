#!/usr/bin/env bash

git log -n 1 | sed '/\(commit\|Author\|Date\|Merge:\|Merge branch\|See merge\|^[ ]*$\)/d'