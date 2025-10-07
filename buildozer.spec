[app]
# Название приложения
title = Графики функций
# Имя пакета (должно быть уникальным)
package.name = graphbuilder
# Название приложения для отображения
package.domain = com.graphicbuilder

# Версии
version = 1.0
# Номер версии для маркета (должен увеличиваться с каждым обновлением)
version.code = 1

# Путь к главному файлу
source.dir = .
# Главный файл приложения
source.include_exts = py,png,jpg,kv,atlas,txt

# Главный класс приложения
main = main.py

# Требуемая версия Python
requirements = python3,kivy,numpy,math

# Версия Android SDK
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b

# Разрешения
android.permissions = INTERNET

# Характеристики приложения
android.arch = armeabi-v7a,arm64-v8a

# Иконка (должна быть в папке с проектом)
# icon.filename = icon.png

# Пресет для ориентации экрана
orientation = portrait

# Настройки полноэкранного режима
fullscreen = 0

# Настройки окна
window.show_title = 1
window.softinput_mode = resize

# Ключ для подписи (для отладки)
android.release_artifact = .apk
presplash.filename = %(source.dir)s/presplash.png

# Логирование
log_level = 2

# Пакеты для включения в сборку
android.add_src = 

# Исключения
android.exclude_exts = _

# Дополнительные настройки Kivy
android.entrypoint = org.kivy.android.PythonActivity
android.meta_data = 
android.intent_filters = 

# Настройки для numpy и других библиотек
android.gradle_dependencies = 
android.add_gradle_repositories = 
android.gradle_plugins = 

# Дополнительные файлы
android.add_resources = 
android.manifest = 
android.allow_backup = true
android.filename = GraphBuilder-{version}.apk

[buildozer]
# Версия buildozer
log_level = 2
warn_on_root = 1

# Дополнительные настройки
android.accept_sdk_license = True