import sqlite3

# Lê o arquivo schema.sql
with open('schema.sql', 'r', encoding='utf-8') as file:
    schema_sql = file.read()

# Conecta ao banco de dados
conn = sqlite3.connect('comandos.db')
cursor = conn.cursor()

# Executa o SQL
try:
    cursor.executescript(schema_sql)
    conn.commit()
    print("✅ Schema executado com sucesso!")
    print("📋 Tabelas criadas:")
    
    # Verifica tabelas criadas
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")
        
except Exception as e:
    print(f"❌ Erro ao executar schema: {e}")
    conn.rollback()
finally:
    conn.close()
