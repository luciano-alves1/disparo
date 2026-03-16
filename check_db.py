import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('comandos.db')
cursor = conn.cursor()

# Verifica se as tabelas existem
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()

print("Tabelas encontradas:")
for table in tables:
    print(f"- {table[0]}")

# Se a tabela existe, mostra a estrutura
if any('comandos_executados' in table for table in tables):
    print("\nEstrutura da tabela 'comandos_executados':")
    cursor.execute('PRAGMA table_info(comandos_executados)')
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Mostra quantidade de registros
    cursor.execute('SELECT COUNT(*) FROM comandos_executados')
    count = cursor.fetchone()[0]
    print(f"\nQuantidade de registros: {count}")
else:
    print("\n❌ Tabela 'comandos_executados' não encontrada!")

conn.close()
