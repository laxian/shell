
# alpha dev internal release
ENV := 
DEVICE_ID := 
ROBOT_ID := 
ROBOT_KEY := 
PROJ_ROOT := .

WORKDIR := $(PROJ_ROOT)
HOST_FILE := app/src/main/java/com/ssssss/robot/cabinet/http/RxHttp.java
PKG_NAME := com.ssssss.robot.cabinet
CONFIG_FILE := '{"NavServicURL":"SSL_PATH","EnableLog":true}'
HOST_PATTERN := https\?://[a-z-]\+\.lllll\.com
CONFIG_PATH := /sdcard/GX/config.json

HOST_ALPHA := https://alpha-cube.lllll.com
SSL_ALPHA := ssl://000.92.80.43:8884
HOST_DEV := https://dev-cube.lllll.com
SSL_DEV := ssl://000.131.2.136:8884
HOST_INTERNAL := https://internal-cube.lllll.com
SSL_INTERNAL := ssl://000.131.2.136:8885
HOST_RELEASE := https://cube.lllll.com
SSL_RELEASE := ssl://000.131.12.142:8884
# alpha debug release
APK_DIR := alpha

ifeq ($(ENV),alpha)
	HOST=$(HOST_ALPHA)
	SSL=$(SSL_ALPHA)
else ifeq ($(ENV),dev)
	HOST=$(HOST_DEV)
	SSL=$(SSL_DEV)
else ifeq ($(ENV),internal)
	HOST=$(HOST_INTERNAL)
	SSL=$(SSL_INTERNAL)
else ifeq ($(ENV),release)
	HOST=$(HOST_RELEASE)
	SSL=$(SSL_RELEASE)
endif

ifeq ($(ENV),internal)
	APK_DIR = release
else ifeq ($(ENV),dev)
	APK_DIR = debug
else
	APK_DIR = $(ENV)
endif

.PHONY: build clean

all: install mqtt key reboot

host:
	sed -i "/String host/s#$(HOST_PATTERN)#$(HOST)#g" $(PROJ_ROOT)/$(HOST_FILE)

build: host clean
	@if [ $(ENV) = "alpha" ]; \
	then \
		$(PROJ_ROOT)/gradlew assembleAlpha -p $(PROJ_ROOT); \
	elif [ $(ENV) = "dev" ]; \
	then \
		$(PROJ_ROOT)/gradlew assembleDebug -p $(PROJ_ROOT); \
	else \
		$(PROJ_ROOT)/gradlew assembleRelease -p $(PROJ_ROOT); \
	fi

install: build
	-adb -s $(DEVICE_ID) uninstall $(PKG_NAME)
	adb -s $(DEVICE_ID) install -r $(PROJ_ROOT)/app/build/outputs/apk/$(APK_DIR)/*.apk

mqtt:
	echo $(CONFIG_FILE) | sed s#SSL_PATH#$(SSL)#g > config.json
	adb -s $(DEVICE_ID) push config.json $(CONFIG_PATH)
	rm config.json

key:
	adb -s $(DEVICE_ID) shell settings put secure robot_id $(ROBOT_ID)
	adb -s $(DEVICE_ID) shell settings put secure robot_key $(ROBOT_KEY)   

reboot:
	adb -s $(DEVICE_ID) reboot

clean:
	$(PROJ_ROOT)/gradlew clean -p $(PROJ_ROOT)