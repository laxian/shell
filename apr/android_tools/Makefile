

run: push_hello
	# adb shell "export CLASSPATH=/sdcard/Hello.dex && exec app_process / src.Hello" 
	adb shell dalvikvm -cp /sdcard/Hello.dex src.Hello

build_hello_java:
	javac src/Hello.java -d bin

build_hello_dx: build_hello_java
	pushd bin && $$ANDROID_HOME/build-tools/27.0.1/dx --dex --output=Hello.dex src/Hello.class && popd

push_hello: build_hello_dx
	adb push bin/Hello.dex /sdcard/

run_ping:
	@echo "Building android tools"
	# @$(MAKE) -C $(ANDROID_TOOLS_DIR) build
	mkdir -p bin
	javac src/Ping.java -d bin
	pushd bin &&/Users/leochou/Library/android/sdk/build-tools/27.0.1/dx --dex --output=Ping.dex src/Ping.class && popd
	adb push bin/Ping.dex /sdcard/
	adb shell dalvikvm -cp /sdcard/Ping.dex src.Ping $$ip

