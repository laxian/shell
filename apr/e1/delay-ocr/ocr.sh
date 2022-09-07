#!/bin/bash

workdir=$(
    cd $(dirname $0)
    pwd
)

if [ $# -eq 0 ]; then
	cat << EOF
	Usage: ocr.sh <path-to-video-file> [path-to-output]
EOF
	exit 1
fi

VIDEO=$1

if [ ! -f "$VIDEO" ]; then
	echo "File \"$VIDEO\" do not exists, exit"
	exit 2
fi

if [[ -n $2 ]]; then
	OUTPUT_DIR=$2
	echo "output dir: $OUTPUT_DIR"
else
	OUTPUT_DIR=${VIDEO%.*}
fi
OUTPUT_DIR=${OUTPUT_DIR:-tmp}

if [ -d "${OUTPUT_DIR}" ]; then
	echo "${OUTPUT_DIR} already exists, skipping or overwrite it(y/n)?"
	read -p "${OUTPUT_DIR} already exists, skipping or overwrite it(y/n)?" goahead >/dev/null 2>&1
	if [[ $goahead == 'yes' || $goahead == 'y' ]]; then
		echo "You input YES, continue..."
	else
		echo "You input NO, exit"
		exit 3
	fi
else
	echo "creating directory ${OUTPUT_DIR}"
	mkdir -p "${OUTPUT_DIR}"
fi

if [ "$(command -v ffmpeg)" ]; then
	ffmpeg -i $1 -r 5 -f image2 $OUTPUT_DIR/1_frame_%05d.bmp
else
	echo "ffmpeg not found, exit"
	exit 4
fi

clear
echo "Start ocr..."

# works on Mac OS X, but grep on linux do not support \d
# python paddle_ocr.py $OUTPUT_DIR | grep -E "^(\d{2}[:.]){3}\d{3},(\d{2}[:.]){3}\d{3},\d{2,}$"
# works on Linux
python $workdir/paddle_ocr.py $OUTPUT_DIR | grep -E "([0-9]{2}[:.]){3}[0-9]{3},([0-9]{2}[:.]){3}[0-9]{3},[0-9]{2,}"
#| xargs -n2 | sed 's/ /,/'
