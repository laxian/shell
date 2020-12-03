#!/usr/bin/env bash

#----------------------------------------------------------------
https://www.codewars.com/kata/5539fecef69c483c5a000015/solutions/shell
#----------------------------------------------------------------

set -eu -o pipefail

remove_palindromes () {
  local lines
  lines=$(cat)
  paste -d' ' <(echo "$lines") <(rev <<<"$lines") \
    | (grep -Ev '^([0-9]+) \1$' || true) | cut -d' ' -f1
}

filter_primes () {
  factor | (grep -E '^[0-9]+: [0-9]+$' || true) | cut -d: -f1
}

seq "$1" "$2" \
  | remove_palindromes \
  | filter_primes \
  | rev \
  | filter_primes \
  | rev \
  | paste -s -d' ' - \
  | (grep -v '^$' || true)