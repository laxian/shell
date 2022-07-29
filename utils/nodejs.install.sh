#!/usr/bin/env bash

#----------------------
# nodejs install script，for Linux and Mac，any arch
# by weixian.zhou
#----------------------


function log () {
	echo "=== $1 ==="
}

# NODEJS_VERSION="v16.16.0"
NODEJS_VERSION=`curl -s https://nodejs.org/en/download/ \
| grep tar.gz \
| sed -n 's#.*\(https\?:\/\/[a-zA-Z0-9/\.-]\+\).*#\1#;p' \
| head -1 \
| sed 's#.*\(v[0-9\.]\+\).*#\1#' \
| sed 's;\.$;;'`
log "Newest version is ${NODEJS_VERSION}"

if [ "$(command -v node)" ]; then
	node_version=`node -v`
	log "nodejs-${node_version} exists on system"
	log "Do you want to install nodejs anyway? yes or not?"
	read goahead </dev/tty
	if [[ $goahead == 'yes' || $goahead == 'y' ]]; then
		log "you choosed yes"
		has_node=1
	else
		log "you exited install"
		exit 0
	fi
fi

_ARCH=`arch`
# x86_64 arch => x64
ARCH=${_ARCH/86_/}
log "Your CPU Arch is ${ARCH}"

# System support linux or Mac(darwin)
SYS=linux
darwin=false
case "`uname`" in
  Darwin* )
    SYS=darwin
    ;;
esac
log "Your System is $SYS"

URL=https://nodejs.org/dist/${NODEJS_VERSION}/node-${NODEJS_VERSION}-${SYS}-${ARCH}.tar.xz
INSTALL_DIR=/opt

# node-v16.15.1-linux-arm64.tar.xz
FILENAME=${URL##*/}
DIRNAME=${FILENAME/.tar.xz/}

echo $DIRNAME

[ -d ./tmp ] || mkdir tmp

if [ -f $FILENAME ]; then
	log "File ${FILENAME} exists"
	cp $FILENAME tmp/
else
	log "Downloading...${URL}"
	curl -SLO $URL
	if [ $? != 0 ]; then
		log "download nodejs error"
		exit 1
	else
		cp $FILENAME tmp/
	fi
fi

cd tmp

log "start uncompress"
tar -xf $FILENAME

xv_result=$?
if [[ $xv_result != 0 ]];then
	log "Uncompress $FILENAME ERROR, exit $xv_result, please try again"
	rm ../$FILENAME
	exit 4
fi

log "start install, need admin password"
if [ -d $INSTALL_DIR/nodejs ]; then
	log "$INSTALL_DIR/nodejs exists, make sure override it? yes or skip or cancel?"
	read goahead </dev/tty
	while :; do
		log "you input $goahead"
		if [[ $goahead == 'yes' || $goahead == 'y' ]]; then
			log "[overwrite] mv $DIRNAME nodejs to $INSTALL_DIR"
			sudo rm -rf $INSTALL_DIR/nodejs
			sudo mv $DIRNAME $INSTALL_DIR/nodejs
			break
		elif [[ $goahead == 'skip' ]]; then
			resolved=2
			if [ has_node == 1 ]; then
				log "you skipped, use old node version"
				exit 2
			fi
			break
		elif [[ $goahead == 'cancel' ]]; then
			log "you canceled install, exit"
			exit 3
		else
			unset goahead
			log "unsupport input, input again!"
		fi
	done
else
	log "install $DIRNAME to $INSTALL_DIR/"
	sudo mv $DIRNAME $INSTALL_DIR/nodejs
fi

log "add to PATH"
grep "NODE_DIR=/opt/nodejs" ~/.bashrc || echo -e "\nexport NODE_DIR=/opt/nodejs" >> ~/.bashrc
grep "PATH=\$NODE_DIR/bin:\$PATH" ~/.bashrc || echo "export PATH=\$NODE_DIR/bin:\$PATH" >> ~/.bashrc

log "clean..."
cd ..
rm -rf tmp
source ~/.bashrc
node -v

if [ $? == 0 ]; then
	log "well done!"
else
	log "install failed"
fi
