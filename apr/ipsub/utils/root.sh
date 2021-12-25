#!/usr/bin/env bash -x

#----------------------------
# 解除只读，然后重启
#----------------------------

# -----------ROOT-----------
adb root
adb remount
adb disable-verity
adb reboot
# -----------ROOT-----------