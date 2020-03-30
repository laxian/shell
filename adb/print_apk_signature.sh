#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo 'Error: Filepath to APK is undefined.'
  exit 1
fi

apk_path="$1"

if [ ! -z "$2" ]; then
  fingerprint="$2"

  case "$fingerprint" in
    MD5|SHA-1|SHA-256)
      ;;
    *)
      echo 'Error: fingerprint_hash_algorithm is invalid.'
      exit 1
      ;;
  esac
fi

apksigner_jar="/Users/leochou/Library/Android/sdk/build-tools/29.0.0/lib/apksigner.jar"

if [ -z "$fingerprint" ]; then
  java -jar "$apksigner_jar" verify --print-certs -v "$apk_path"
else
  (
    IFS=$'\n'
    filter="Signer #1 certificate ${fingerprint} digest:"
    for line in `java -jar "$apksigner_jar" verify --print-certs "$apk_path"`; do
      filtered_line="${line/$filter/}"

      if [ ! "$line" == "$filtered_line" ]; then
        filtered_line="${filtered_line//[^0-9a-fA-F]/}"

        if [ ! -z "$filtered_line" ]; then
          echo "$filtered_line"
          break
        fi
      fi
    done
  )
fi