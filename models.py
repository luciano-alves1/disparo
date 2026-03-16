import sqlite3
from datetime import datetime
from typing import List, Optional

class Database:
    """Classe para gerenciar conexão e operações com o banco de dados SQLite"""
    
    def __init__(self, db_file: str = "comandos.db"):
        self.db_file = db_file
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_file)
    
    def init_database(self):
        """Inicializa o banco de dados criando as tabelas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Cria tabela de comandos executados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comandos_executados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comando VARCHAR(500) NOT NULL,
                saida_completa TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'sucesso'
            )
        ''')
        
        # Cria índice para melhorar performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON comandos_executados(timestamp)
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Banco de dados '{self.db_file}' inicializado com sucesso!")

class ComandoExecutado:
    """Model para representar um comando executado"""
    
    def __init__(self, id: Optional[int] = None, comando: str = "", 
                 saida_completa: str = "", timestamp: Optional[datetime] = None, 
                 status: str = "sucesso"):
        self.id = id
        self.comando = comando
        self.saida_completa = saida_completa
        self.timestamp = timestamp or datetime.now()
        self.status = status
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'comando': self.comando,
            'saida_completa': self.saida_completa,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ComandoExecutado':
        """Cria objeto a partir de um dicionário"""
        return cls(
            id=data.get('id'),
            comando=data.get('comando', ''),
            saida_completa=data.get('saida_completa', ''),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else None,
            status=data.get('status', 'sucesso')
        )
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'ComandoExecutado':
        """Cria objeto a partir de uma linha do banco de dados"""
        return cls(
            id=row[0],
            comando=row[1],
            saida_completa=row[2],
            timestamp=datetime.fromisoformat(row[3]) if row[3] else None,
            status=row[4]
        )

class ComandoRepository:
    """Repositório para operações com comandos executados"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def salvar(self, comando: ComandoExecutado) -> int:
        """Salva um comando no banco de dados e retorna o ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO comandos_executados (comando, saida_completa, status)
            VALUES (?, ?, ?)
        ''', (comando.comando, comando.saida_completa, comando.status))
        
        comando_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        comando.id = comando_id
        return comando_id
    
    def buscar_todos(self, limit: Optional[int] = None) -> List[ComandoExecutado]:
        """Busca todos os comandos executados"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, comando, saida_completa, timestamp, status 
            FROM comandos_executados 
            ORDER BY timestamp DESC
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [ComandoExecutado.from_db_row(row) for row in rows]
    
    def buscar_por_id(self, comando_id: int) -> Optional[ComandoExecutado]:
        """Busca um comando pelo ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, comando, saida_completa, timestamp, status 
            FROM comandos_executados 
            WHERE id = ?
        ''', (comando_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return ComandoExecutado.from_db_row(row)
        return None
    
    def buscar_recentes(self, limit: int = 10) -> List[ComandoExecutado]:
        """Busca os comandos mais recentes"""
        return self.buscar_todos(limit=limit)
    
    def deletar_todos(self) -> int:
        """Deleta todos os registros e retorna a quantidade deletada"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM comandos_executados')
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted_count

# Configuração global do banco de dados
database = Database()
comando_repo = ComandoRepository(database)

# Funções de conveniência para uso em outras partes do código
def init_db():
    """Inicializa o banco de dados (compatibilidade com código existente)"""
    database.init_database()

def salvar_comando(comando: str, saida: str, status: str = "sucesso") -> int:
    """Salva um comando no banco (função de conveniência)"""
    cmd = ComandoExecutado(comando=comando, saida_completa=saida, status=status)
    return comando_repo.salvar(cmd)

def buscar_historico(limit: int = 10) -> List[dict]:
    """Busca histórico de comandos (função de conveniência)"""
    comandos = comando_repo.buscar_recentes(limit)
    return [cmd.to_dict() for cmd in comandos]

def listar_todos_comandos() -> dict:
    """Lista todos os comandos (função de conveniência)"""
    comandos = comando_repo.buscar_todos()
    return {"total": len(comandos), "comandos": [cmd.to_dict() for cmd in comandos]}