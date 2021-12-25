#!/usr/bin/env bash


adb root
adb remount

adb shell rm 
adb shell rm /oem/bundled_persist-app/GxAppService-release-signed/GxAppService-release-signed.apk
adb shell rm /oem/bundled_persist-app/monitor-signed/monitor-signed.apk
adb shell rm /oem/bundled_persist-app/gx-locomotion-signed/gx-locomotion-signed.apk
adb shell rm /oem/bundled_persist-app/Ota/Ota.apk
adb shell rm /oem/bundled_persist-app/visionservicechecker/visionservicechecker.apk
adb shell rm /oem/bundled_persist-app/connectivity-signed/connectivity-signed.apk
adb shell rm /oem/bundled_persist-app/watchdog-signed/watchdog-signed.apk
adb shell rm /oem/bundled_persist-app/GXTools/GXTools.apk
adb shell rm /oem/bundled_persist-app/MirrorControl-release-signed/MirrorControl-release-signed.apk
adb shell rm /oem/bundled_persist-app/checklist-signed/checklist-signed.apk
adb shell rm /oem/bundled_persist-app/voice-signed/voice-signed.apk
adb shell rm /oem/bundled_persist-app/store-signed/store-signed.apk
adb shell rm /oem/bundled_persist-app/debug-log-service-signed/debug-log-service-signed.apk
adb shell rm /oem/bundled_persist-app/remoteota/remoteota.apk
adb shell rm /oem/bundled_persist-app/message-service-signed/message-service-signed.apk
adb shell rm /oem/bundled_persist-app/remote-control-signed/remote-control-signed.apk
adb shell rm /oem/bundled_persist-app/vision-service-signed/vision-service-signed.apk
adb shell rm /oem/bundled_persist-app/robot-config-signed/robot-config-signed.apk