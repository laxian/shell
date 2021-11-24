#!/usr/bin/env bash -x

# --------------------------------------
# NEED ROOT - REMOUNT - DISVERITY FIRST
# SEE ./root.sh
# 删除下面列出的8个内置App
# --------------------------------------

# -----------REMOVE S2 Nav Board-----------
adb root
adb remount

# SegwayProvision
# nav_app
# messageservice
# debuglog
# watchdog
# robotconfig
# GXMonitor
# RobotStore

adb shell rm -rf /oem/bundled_persist-app/message-service-signed
adb shell rm -rf /oem/bundled_persist-app/debug-log-service-signed
adb shell rm -rf /oem/bundled_persist-app/monitor-signed
adb shell rm -rf /oem/bundled_persist-app/watchdog-signed
adb shell rm -rf /oem/bundled_persist-app/store-signed
adb shell rm -rf /oem/bundled_persist-app/robot-config-signed
adb shell rm -rf /oem/bundled_persist-app/GxAppService-release-signed




# adb shell rm -rf /oem/bundled_persist-app/connectivity-signed
# adb shell rm -rf /oem/bundled_persist-app/remoteota
# adb shell rm -rf /oem/bundled_persist-app/MirrorControl-release-signed
# adb shell rm -rf /oem/bundled_persist-app/vision-service-signed
# adb shell rm -rf /oem/bundled_persist-app/visionservicechecker
# adb shell rm -rf /oem/bundled_persist-app/voice-signed
# adb shell rm -rf /oem/bundled_persist-app/checklist-signed
# adb shell rm -rf /oem/bundled_persist-app/gx-locomotion-signed
# adb shell rm -rf /oem/bundled_persist-app/GXTools
# adb shell rm -rf /oem/bundled_persist-app/Ota
# adb shell rm -rf /oem/bundled_persist-app/RockerRobot
# adb shell rm -rf /oem/bundled_persist-app/remote-control-signed
# -----------REMOVE-----------

# -----------RESTART-----------
adb reboot
# -----------RESTART-----------