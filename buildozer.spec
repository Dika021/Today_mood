[app]
title = حال امروز
package.name = todaymood
package.domain = com.alihal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,arabic-reshaper,python-bidi,pyjnius
orientation = portrait
fullscreen = 1
android.api = 35
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
