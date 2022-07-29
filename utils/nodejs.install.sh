#!/usr/bin/env bash


function log () {
	echo "=== $1 ==="
}

if [ "$(command -v node)" ]; then
	node_version=`node -v`
	log "nodejs-${node_version} exists on system"
	log "Do you want to install nodejs anyway? yes or not?"
	read -s goahead
	if [[ $goahead == 'yes' || $goahead == 'y' ]]; then
		log "you choosed yes"
		has_node=1
	else
		log "you exited install"
		exit 0
	fi
fi

_ARCH=`arch`
ARCH=${_ARCH/86_/}
log "Your CPU Arch is ${ARCH}"

SYS=linux
darwin=false
case "`uname`" in
  Darwin* )
    SYS=darwin
    ;;
esac
log "Your System is $SYS"

URL=https://nodejs.org/dist/v16.16.0/node-v16.16.0-${SYS}-${ARCH}.tar.xz
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

log "start install, need admin password"
if [ -d $INSTALL_DIR/nodejs ]; then
	log "$INSTALL_DIR/nodejs exists, make sure override it? yes or skip or cancel?"
	read -s goahead
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
grep "PATH=\$PATH:\$NODE_DIR/bin" ~/.bashrc || echo "export PATH=\$PATH:\$NODE_DIR/bin" >> ~/.bashrc

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
