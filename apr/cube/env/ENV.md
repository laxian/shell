# 配送站环境配置手册

#### 配置参数
配置一个配送站新环境，所需参数。一般来说，只需指定:

`ENV`、`DEVICE_ID`、`ROBOT_ID`、`ROBOT_KEY`。

其中`DEVICE_ID`是Android ID，通过`adb devices`获取。

    # alpha dev internal release
    ENV := 
    DEVICE_ID := 
    ROBOT_ID := 
    ROBOT_KEY := 

    PROJ_ROOT := .
    HOST_FILE := app/src/main/java/com/ssssss/robot/cabinet/http/RxHttp.java
    CONFIG_FILE := '{"NavServicURL":"SSL_PATH","EnableLog":true}'
    
    HOST_PATTERN := http://.\+\.lllll\.com
    CONFIG_PATH := /sdcard/GX/config.json
    HOST_ALPHA := http://alpha-cube.lllll.com
    SSL_ALPHA := ssl://000.92.80.43:8884
    HOST_DEV := http://dev-cube.lllll.com
    SSL_DEV := ssl://000.131.2.136:8884
    HOST_INTERNAL := http://internal-cube.lllll.com
    SSL_INTERNAL := ssl://000.131.2.136:8885
    HOST_RELEASE := http://cube.lllll.com
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

#### 1. 切换 http地址
host url，并没有在gradle配置，需要手动修改，在RxHttp.java中

	sed -i "s#$(HOST_PATTERN)#$(HOST)#g" $(PROJ_ROOT)/$(HOST_FILE)

#### 2. 切换 Build Variant
不同的环境对应不同的打包（buildType）

| 环境 | buildType                                           |
|-----|----------------------------------------------------|
| alpha  | alpha                 |
| dev  | debug                             |
| internal  | internal |
| release  | release |

	@if [ $(ENV) = "alpha" ]; \
	then \
		$(PROJ_ROOT)/gradlew assembleAlpha; \
	elif [ $(ENV) = "dev" ]; \
	then \
		$(PROJ_ROOT)/gradlew assembleDebug; \
	else \
		$(PROJ_ROOT)/gradlew assembleRelease; \
	fi

    # install apk
	adb -s $(DEVICE_ID) install -r $(PROJ_ROOT)/app/build/outputs/apk/$(APK_DIR)/*.apk


#### 3. 切换 MQTT地址
MQTT地址配置在设备/sdcard/GX/config.json，格式如：`{"NavServicURL":"SSL_PATH","EnableLog":true}`

	echo $(CONFIG_FILE) | sed s#SSL_PATH#$(SSL_PATH)#g > config.json
	adb -s $(DEVICE_ID) push config.json /sdcard/GX/config.json

#### 4. Android设备设置robot_id/robot_key
这两个字段，配置在Android Settings里，adb 提供了操作命令。也可以手动修改。

旧版本Android，位置在：`/data/data/com.android.providers.settings/databases/settings.db `。

新版本在： /data/system/users/0目录下，该目录的settings_global.xml，settings_secure.xml和settings_system.xml三个xml文件就是SettingsProvider中的数据文件。这里使用的是：xml，settings_secure.xml

	adb -s $(DEVICE_ID) shell settings put secure robot_id $(ROBOT_ID)
	adb -s $(DEVICE_ID) shell settings put secure robot_key $(ROBOT_KEY)

#### 5. 重启设备使MQTT生效
	adb -s $(DEVICE_ID) reboot

#### REF

[配送站硬件激活流程](https://wiki.ssssssrobotics.com/pages/viewpage.action?pageId=53599655)

[配送站后台](https://wiki.ssssssrobotics.com/pages/viewpage.action?pageId=50279650)


#### Makefile
使用方法：

1. 配置ENV等参数
2. make

```Makefile
# alpha dev internal release
ENV := 
DEVICE_ID := 
ROBOT_ID := 
ROBOT_KEY := 
PROJ_ROOT := /Users/leochou/app-apr-cabinet/GxCabinetApp

WORKDIR := $(PROJ_ROOT)
HOST_FILE := app/src/main/java/com/ssssss/robot/cabinet/http/RxHttp.java
PKG_NAME := com.ssssss.robot.cabinet
CONFIG_FILE := '{"NavServicURL":"SSL_PATH","EnableLog":true}'
HOST_PATTERN := https://[a-z-]\+\.lllll\.com
CONFIG_PATH := /sdcard/GX/config.json

SEG1 := `cat .private`
HOST_ALPHA := http://alpha-cube.lllll.com
SSL_ALPHA := ssl://000.92.80.43:8884
HOST_DEV := http://dev-cube.lllll.com
SSL_DEV := ssl://000.131.2.136:8884
HOST_INTERNAL := http://internal-cube.lllll.com
SSL_INTERNAL := ssl://000.131.2.136:8885
HOST_RELEASE := http://cube.lllll.com
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
	adb -s $(DEVICE_ID) uninstall $(PKG_NAME)
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
```


#### shell
```bash
#!/usr/bin/env bash -x

# alpha dev internal release
CUBE_ENV=
DEVICE_ID=
ROBOT_ID=
ROBOT_KEY=

PROJ_ROOT=/Users/leochou/app-apr-cabinet/GxCabinetApp
HOST_FILE=app/src/main/java/com/ssssss/robot/cabinet/http/RxHttp.java
PKG_NAME=com.ssssss.robot.cabinet
CONFIG_FILE='{"NavServicURL":"SSL_PATH","EnableLog":true}'
HOST_PATTERN="https://[a-z-]\+\.lllll\.com"
CONFIG_PATH=/sdcard/GX/config.json

HOST_ALPHA=http://alpha-cube.lllll.com
SSL_ALPHA=ssl://000.92.80.43:8884
HOST_DEV=http://dev-cube.lllll.com
SSL_DEV=ssl://000.131.2.136:8884
HOST_INTERNAL=http://internal-cube.lllll.com
SSL_INTERNAL=ssl://000.131.2.136:8885
HOST_RELEASE=http://cube.lllll.com
SSL_RELEASE=ssl://000.131.12.142:8884
# alpha debug release
APK_DIR=alpha

if [ $CUBE_ENV = "alpha" ]; then
    HOST=$HOST_ALPHA
    SSL=$SSL_ALPHA
elif [ $CUBE_ENV = "dev" ]; then
    HOST=$HOST_DEV
    SSL=$SSL_DEV
elif [ $CUBE_ENV = "internal" ]; then
    HOST=$HOST_INTERNAL
    SSL=$SSL_INTERNAL
elif [ $CUBE_ENV = "release" ]; then
    HOST=$HOST_RELEASE
    SSL=$SSL_RELEASE
fi

if [ $CUBE_ENV = "internal" ]; then
    APK_DIR=release
elif [ $CUBE_ENV = "dev" ]; then
    APK_DIR=debug
else
    APK_DIR=$CUBE_ENV
fi

# 修改host
sed -i "/String host/s#$HOST_PATTERN#$HOST#g" $PROJ_ROOT/$HOST_FILE

# build
pushd $PROJ_ROOT
if [ $CUBE_ENV = "alpha" ]; then
    $PROJ_ROOT/gradlew clean assembleAlpha
elif [ $CUBE_ENV = "dev" ]; then
    $PROJ_ROOT/gradlew clean assembleDebug
else
    $PROJ_ROOT/gradlew clean assembleRelease
fi
popd

# install
adb -s $DEVICE_ID uninstall $PKG_NAME
adb -s $DEVICE_ID install -r $PROJ_ROOT/app/build/outputs/apk/$APK_DIR/*.apk

# config MQTT ssl
echo $CONFIG_FILE | sed "s#SSL_PATH#$SSL#g" > config.json
adb -s $DEVICE_ID push config.json $CONFIG_PATH
rm config.json

# set robot_id/robot_key
adb -s $DEVICE_ID shell settings put secure robot_id $ROBOT_ID
adb -s $DEVICE_ID shell settings put secure robot_key $ROBOT_KEY

# reboot device
adb -s $DEVICE_ID reboot

```