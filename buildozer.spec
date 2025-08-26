[app]
title = Mapa do Marianoto
package.name = marianoto
package.domain = com.marianoto

source.dir = .
source.main = main.py

# ✅ LISTA EXPLÍCITA DE TODAS AS IMAGENS
source.include_exts = py,png,jpg,jpeg
source.include_patterns = 
    mari.png,
    mari_walk.png,
    mari_up.png, 
    mari_down.png,
    mari_attack.png,
    chest.png

version = 1.0
requirements = python3, pygame

orientation = landscape
android.api = 29
android.minapi = 21
