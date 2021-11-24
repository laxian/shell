#!/usr/bin/env bash -x

# -----------ROOT-----------
adb root
adb remount
adb disable-verity
adb reboot
# -----------ROOT-----------