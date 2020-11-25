package_name := <package_name>
path_to_activity := <path_to_activity>

.PHONY: build clean

all: build mock andserver
	echo build successful

mock:
	@npm run dev --prefix ./libraries/mock

andserver:
	./hw_ip.sh

build:
	./gradlew :app:assembleDebug
	adb -d install -r -t app/build/outputs/apk/debug/*.apk
	adb -d shell am start -n "$(package_name)/$(package_name).$(path_to_activity)" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER

uninstall:
	adb -d uninstall ${package_name}

setup: private/package_name private/path_to_activity
	./replace_package_name.sh

test:
	echo test

clean:
	./gradlew clean