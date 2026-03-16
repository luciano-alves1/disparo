#!/usr/bin/env python3
"""
Teste de conexão com PostgreSQL
Execute este script para verificar se a conexão com seu banco PostgreSQL está funcionando
"""

import os
from dotenv import load_dotenv
import psycopg2

# Carrega variáveis de ambiente
load_dotenv()

def test_postgres_connection():
    """Testa conexão com PostgreSQL"""
    try:
        # Pega configurações do .env
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        dbname = os.getenv('DB_NAME', 'seu_banco')
        user = os.getenv('DB_USER', 'seu_usuario')
        password = os.getenv('DB_PASSWORD', 'sua_senha')
        table_name = os.getenv('TABLE_NAME', 'newtable')
        
        print("🔍 Testando conexão com PostgreSQL...")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {dbname}")
        print(f"   User: {user}")
        print(f"   Table: {table_name}")
        print()
        
        # Tenta conectar
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        
        cursor = conn.cursor()
        
        # Verifica se a tabela existe
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = %s
        """, (table_name,))
        
        table_exists = cursor.fetchone()
        
        if table_exists:
            print(f"✅ Tabela '{table_name}' encontrada!")
            
            # Mostra estrutura da tabela
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            
            columns = cursor.fetchall()
            print("\n📋 Estrutura da tabela:")
            for col in columns:
                print(f"   - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
                
            # Conta registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n📊 Quantidade de registros: {count}")
            
        else:
            print(f"❌ Tabela '{table_name}' não encontrada!")
            print(f"🔧 Criando tabela '{table_name}'...")
            
            # Cria tabela
            cursor.execute(f'''
                CREATE TABLE {table_name} (
                    id SERIAL PRIMARY KEY,
                    comando VARCHAR(500) NOT NULL,
                    saida_completa TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'sucesso'
                )
            ''')
            
            # Cria índice
            cursor.execute(f'''
                CREATE INDEX IF NOT EXISTS idx_{table_name}_timestamp 
                ON {table_name}(timestamp)
            ''')
            
            conn.commit()
            print(f"✅ Tabela '{table_name}' criada com sucesso!")
        
        conn.close()
        print("\n🎉 Conexão com PostgreSQL estabelecida com sucesso!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Erro de conexão com PostgreSQL: {e}")
        print("\n🔧 Verifique:")
        print("   1. Se o PostgreSQL está rodando")
        print("   2. Se as credenciais no .env estão corretas")
        print("   3. Se o banco de dados existe")
        print("   4. Se o usuário tem permissão de acesso")
        return False
        
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    test_postgres_connection()
