#!/bin/bash -x
IFS=$',\n'
travel() {
    narrowed=()
    for address in $ad; do
      if [[ "${address: -8}" == "$2" ]]; then
        narrowed+=($address)
      fi
    done
    numbers=()
    street=()
    for address in ${narrowed[@]}; do
      numbers+=(${address%% *})
      mid=${address#* }
      street+=(${mid:: -9})
    done
    echo "$2:${street[*]}/${numbers[*]}"
}
travel "$1" "$2"