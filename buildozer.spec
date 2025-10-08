[app]
title = Graph Plotter
package.name = graphplotter
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0,numpy==1.24.4,cython==0.29.33
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.arch = armeabi-v7a
android.permissions = INTERNET
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1

# Используем стабильные версии
p4a.branch = develop
android.ndk = 25b
android.sdk = 33