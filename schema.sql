-- Schema SQL para criar tabela de comandos executados
CREATE TABLE IF NOT EXISTS comandos_executados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comando VARCHAR(500) NOT NULL,
    saida_completa TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'sucesso'
);

-- Índice para melhorar performance
CREATE INDEX IF NOT EXISTS idx_timestamp ON comandos_executados(timestamp);
