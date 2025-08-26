[app]

title = Mapa Marianoto
package.name = mapa_marianoto
package.domain = org.gg2210

# Inclui todos os arquivos importantes diretamente
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec

requirements = python3,kivy

orientation = portrait
version = 1.0
android.minapi = 21
android.api = 34
android.build_tools = 34.0.0

p4a.branch = v2024.01.21

icon.filename = %(source.dir)s/icon.png
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE
log_level = 2

# Não há pasta de assets, sprites soltos já estão incluídos
android.add_assets = 

# Força modo debug
android.debug = 1
