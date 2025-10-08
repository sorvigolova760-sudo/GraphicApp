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
android.permissions = INTERNET
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
# Убираем абсолютные пути — Buildozer сам создаст .buildozer/android/platform/*