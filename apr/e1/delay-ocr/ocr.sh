#!/bin/bash


if [ $# -eq 0 ]; then
	cat << EOF
	Usage: ocr.sh <path-to-video-file> [path-to-output]
EOF
fi

OUTPUT_DIR=${2:-tmp}

echo $OUTPUT_DIR

if [ -d "${OUTPUT_DIR}" ]; then
	echo "${OUTPUT_DIR} already exists, skipping or overwrite it(y/n)?"
	read -p "${OUTPUT_DIR} already exists, skipping or overwrite it(y/n)?" goahead >/dev/null 2>&1
	if [[ $goahead == 'yes' || $goahead == 'y' ]]; then
		echo "You input YES, continue..."
	else
		echo "You input NO, exit"
		exit 1
	fi
else
	echo "creating directory ${OUTPUT_DIR}"
	mkdir -p "${OUTPUT_DIR}"
fi

ffmpeg -i $1 -r 5 -f image2 $OUTPUT_DIR/1_frame_%05d.bmp
clear
echo "Start ocr..."
python paddle_ocr.py $OUTPUT_DIR | grep -E "^(\d{2}[:.]){3}\d{3},(\d{2}[:.]){3}\d{3},\d{2,}$"
#| xargs -n2 | sed 's/ /,/'
