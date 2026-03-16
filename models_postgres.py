import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Optional, Dict

# Carrega variáveis de ambiente do arquivo .env
load_dotenv('.env')

class PostgreSQLDatabase:
    """Classe para gerenciar conexão com PostgreSQL"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.dbname = os.getenv('DB_NAME', 'seu_banco')
        self.user = os.getenv('DB_USER', 'seu_usuario')
        self.password = os.getenv('DB_PASSWORD', 'sua_senha')
        self.table_name = os.getenv('TABLE_NAME', 'newtable')
        
    def get_connection(self):
        """Retorna conexão com PostgreSQL"""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )
    
    def init_database(self):
        """Inicializa a tabela no PostgreSQL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Cria tabela se não existir
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id SERIAL PRIMARY KEY,
                comando VARCHAR(500) NOT NULL,
                saida_completa TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'sucesso'
            )
        ''')
        
        # Cria índice
        cursor.execute(f'''
            CREATE INDEX IF NOT EXISTS idx_{self.table_name}_timestamp 
            ON {self.table_name}(timestamp)
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Tabela '{self.table_name}' criada no PostgreSQL!")

class ComandoRepositoryPostgreSQL:
    """Repositório para operações com PostgreSQL"""
    
    def __init__(self, db: PostgreSQLDatabase):
        self.db = db
    
    def salvar(self, comando: str, saida: str, status: str = "sucesso") -> int:
        """Salva um comando no PostgreSQL"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            INSERT INTO {self.db.table_name} (comando, saida_completa, status)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (comando, saida, status))
        
        comando_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return comando_id
    
    def buscar_historico(self, limit: int = 10) -> List[Dict]:
        """Busca histórico de comandos"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(f'''
            SELECT id, comando, saida_completa, timestamp, status 
            FROM {self.db.table_name} 
            ORDER BY timestamp DESC 
            LIMIT %s
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def listar_todos_comandos(self) -> Dict:
        """Lista todos os comandos"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(f'''
            SELECT id, comando, saida_completa, timestamp, status 
            FROM {self.db.table_name} 
            ORDER BY timestamp DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return {"total": len(rows), "comandos": [dict(row) for row in rows]}

# Configuração global
postgres_db = PostgreSQLDatabase()
postgres_repo = ComandoRepositoryPostgreSQL(postgres_db)

# Funções de conveniência
def init_db():
    """Inicializa o banco PostgreSQL"""
    postgres_db.init_database()

def salvar_comando(comando: str, saida: str, status: str = "sucesso") -> int:
    """Salva um comando no PostgreSQL"""
    return postgres_repo.salvar(comando, saida, status)

def buscar_historico(limit: int = 10) -> List[Dict]:
    """Busca histórico do PostgreSQL"""
    return postgres_repo.buscar_historico(limit)

def listar_todos_comandos() -> Dict:
    """Lista todos do PostgreSQL"""
    return postgres_repo.listar_todos_comandos()
