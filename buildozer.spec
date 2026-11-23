[app]

title = Horror Terminal
package.name = horrorterminal
package.domain = org.demo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3==3.12.10,hostpython3==3.12.10,kivy

orientation = portrait
fullscreen = 0

android.permissions =

android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

[buildozer]

log_level = 2
warn_on_root = 1