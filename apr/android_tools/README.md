# Java Android命令行工具

## helloworld

```Java
package src;

public class a {
	public static void main(String[] args) {
		System.out.println("Hello World!");
	}
}
```

```Bash
javac src/Hello.java -d bin
pushd bin && $ANDROID_HOME/build-tools/27.0.1/dx --dex --output=Hello.dex src/Hello.class && popd
adb push bin/Hello.dex /sdcard/
# adb shell "export CLASSPATH=/sdcard/Hello.dex && exec app_process / src.Hello" 
adb shell dalvikvm -cp /sdcard/Hello.dex src.Hello
```


## helloworld cpp

```cpp
$ANDROID_HOME/cmake/3.6.4111459/bin/cmake -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI=arm64-v8a
make
adb push HelloWorld /data/local/tmp 
adb shell /data/local/tmp/HelloWorld
```
