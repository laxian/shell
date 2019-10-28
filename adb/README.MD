
## expert_installed_apk
导出已安装的apk
```shell
# 以豆瓣为例
~ adb shell pm list packages | grep douban
package:com.douban.frodo

~ adb shell pm path com.douban.frodo
package:/data/app/com.douban.frodo-3MPKjrePTfpmBRjP24ESnw==/base.apk

~ adb pull /data/app/com.douban.frodo-3MPKjrePTfpmBRjP24ESnw==/base.apk ./douban.com
/data/app/com.douban.frodo-3MPKjrePTfp.... 38.9 MB/s (41950908 bytes in 1.030s)
➜  ~
```
