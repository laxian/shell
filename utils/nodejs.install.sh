#!/usr/bin/env bash

#------------------------------------------------------------------
# nodejs install script，for Linux and Mac，any arch
# by weixian.zhou
# uninstall: 
# [Danger] sudo rm -rf /opt/nodejs ; rm ~/.bashrc ; sed -i '/.bashrc/c\'  ~/.zshrc
# or uninstall by hand:
# 1. delete /opt/nodejs
# 2. remove ~/.bashrc export statements
# 3. remove ~/.zshrc source statements
#------------------------------------------------------------------

INSTALL_DIR=/opt

function log () {
	echo "=== $1 ==="
}

function exit_clean () {
	cd .. && rm -rf tmp
	exit $1
}

function get_lts_version () {
	NODEJS_VERSION=`curl -s https://nodejs.org/en/download/ \
	| grep tar.gz \
	| sed -n 's#.*\(https\?:\/\/[a-zA-Z0-9/\.-]\+\).*#\1#;p' \
	| head -1 \
	| sed 's#.*\(v[0-9\.]\+\).*#\1#' \
	| sed 's;\.$;;'`
	echo ${NODEJS_VERSION}
	return 0
}

get_lts_version

# NODEJS_VERSION="v16.16.0"
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
		exit_clean 0
	fi
	unset goahead
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

if [ -f $FILENAME ]; then
	log "$FILENAME already exists, copy it"
	mkdir tmp && cd tmp && cp ../$FILENAME .
else
	[ -d ./tmp ] || mkdir tmp && cd tmp
fi

URL=https://nodejs.org/dist/${NODEJS_VERSION}/node-${NODEJS_VERSION}-${SYS}-${ARCH}.tar.xz
log "binary url: $URL"

# node-v16.15.1-linux-arm64.tar.xz
FILENAME=${URL##*/}
DIRNAME=${FILENAME/.tar.xz/}

echo $DIRNAME

if [ -f $FILENAME ]; then
	log "File ${FILENAME} exists"
else
	log "Downloading...${URL}"
	curl -SLO $URL
	if [ $? != 0 ]; then
		log "download nodejs error"
		exit_clean 1
	fi
fi

log "start uncompress"
tar -xf $FILENAME

xv_result=$?
if [[ $xv_result != 0 ]];then
	log "Uncompress $FILENAME ERROR, exit $xv_result, please try again"
	rm $FILENAME
	exit_clean 4
fi

log "start install, need admin password"
if [ -d $INSTALL_DIR/nodejs ]; then
	log "$INSTALL_DIR/nodejs exists, make sure override it? yes or skip or cancel?"
	while :; do
		read goahead </dev/tty
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
				exit_clean 2
			fi
			break
		elif [[ $goahead == 'cancel' ]]; then
			log "you canceled install, exit"
			exit_clean 3
		else
			log "unsupport input, input again!"
			unset goahead
		fi
	done
	unset goahead
else
	log "install $DIRNAME to $INSTALL_DIR/"
	sudo mv $DIRNAME $INSTALL_DIR/nodejs
fi

if [ ! -d "$INSTALL_DIR/nodejs" ]; then
	log "$INSTALL_DIR/nodejs not exists, exit"
	exit_clean 5
fi

log "add to PATH"

PROFILE=~/.bashrc
if [ -f "~/.bashrc" ]; then
	echo "File \"~/.bashrc\" exists"
	PROFILE="~/.bashrc"
elif [[ -f ~/.bash_profile ]];then
	PROFILE="~/.bash_profile"
else
	log "no bash profile found"
fi
log "use profile ${PROFILE}"
touch ${PROFILE}

grep "NODE_DIR=/opt/nodejs" ${PROFILE} >/dev/null || echo -e "\nexport NODE_DIR=/opt/nodejs" >> ${PROFILE}
grep "PATH=\$NODE_DIR/bin:\$PATH" ${PROFILE} >/dev/null || echo "export PATH=\$NODE_DIR/bin:\$PATH" >> ${PROFILE}

if [[ $SHELL == '/bin/zsh' ]]; then
	log "found zsh, add to zsh? y/n"
	read -t 3 goahead </dev/tty
	if [[ $goahead == 'yes' || $goahead == 'y' ]]; then
		grep "source /Users/leochou/.bashrc" ~/.zshrc || echo "source ${PROFILE}" >> ~/.zshrc
		log "add to zsh done"
	else
		log "skip add to zsh"
	fi
	unset goahead
fi

log "clean..."
cd .. && rm -rf ./tmp
source ${PROFILE}
node -v

if [ $? == 0 ]; then
	log "well done!"
else
	log "install failed"
fi
