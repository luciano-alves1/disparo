#!/usr/bin/env python3
"""
Verifica a estrutura real da tabela newtable no PostgreSQL
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Carrega variáveis de ambiente
load_dotenv()

def check_table_structure():
    """Verifica estrutura atual da tabela"""
    try:
        # Conecta ao PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME', 'seu_banco'),
            user=os.getenv('DB_USER', 'seu_usuario'),
            password=os.getenv('DB_PASSWORD', 'sua_senha')
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        table_name = os.getenv('TABLE_NAME', 'newtable')
        
        print(f"🔍 Verificando estrutura da tabela '{table_name}'...")
        
        # Verifica se tabela existe
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = %s
        """, (table_name,))
        
        if not cursor.fetchone():
            print(f"❌ Tabela '{table_name}' não encontrada!")
            return False
        
        # Mostra estrutura atual
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        
        columns = cursor.fetchall()
        
        print(f"\n📋 Estrutura atual da tabela '{table_name}':")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"   - {col['column_name']} ({col['data_type']}) {nullable}{default}")
        
        # Mostra dados recentes se existirem
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        rows = cursor.fetchall()
        
        if rows:
            print(f"\n📊 Dados recentes ({len(rows)} registros):")
            for i, row in enumerate(rows, 1):
                print(f"   Registro {i}: {dict(row)}")
        else:
            print(f"\n📊 Tabela vazia - nenhum registro encontrado")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    check_table_structure()
