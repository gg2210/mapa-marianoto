[app]

# Nome do app
title = Mapa Marianoto
# Nome do pacote (não pode ter espaços)
package.name = mapa_marianoto
# Domínio inverso
package.domain = org.gg2210

# Arquivo principal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec

# Requisitos Python
requirements = python3,kivy

# Orientação da tela
orientation = portrait

# Versão do app
version = 1.0
# Permitir que o app seja rodado em dispositivos com API mínima
android.minapi = 21
# API alvo
android.api = 34
# Build-tools
android.build_tools = 34.0.0

# Python-for-android
p4a.branch = v2024.01.21

# Permitir ícone padrão (se não tiver um, Buildozer gera)
icon.filename = %(source.dir)s/icon.png

# Permissões extras (adicione se precisar)
android.permissions = INTERNET

# Configurações de log e depuração
log_level = 2
