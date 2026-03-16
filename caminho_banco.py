import os

# Caminho completo do banco de dados
caminho_completo = os.path.abspath('comandos.db')
print(f"📍 Caminho completo do banco de dados:")
print(caminho_completo)
print(f"\n📁 Copie este caminho para o DBeaver:")
print(f"File: {caminho_completo}")
print(f"\n🔍 Ou use o caminho relativo:")
print(f"File: comandos.db")
print(f"(se o DBeaver estiver no mesmo diretório)")

# Verifica se o arquivo existe
if os.path.exists('comandos.db'):
    print(f"\n✅ Arquivo existe!")
    print(f"📊 Tamanho: {os.path.getsize('comandos.db')} bytes")
else:
    print(f"\n❌ Arquivo não encontrado!")
