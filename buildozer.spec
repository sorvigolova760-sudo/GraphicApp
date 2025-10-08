[app]
title = Graph Plotter
package.name = graphplotter
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,numpy
orientation = portrait
fullscreen = 1
android.api = 35
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk
android.ndk_api = 21
android.permissions = INTERNET
log_level = 2
# Можно указать иконку, если добавишь:
# icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1