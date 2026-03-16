# 🖥️ Executor de Comandos - Backend API

API RESTful para execução de comandos do sistema com armazenamento em PostgreSQL.

## 🚀 Recursos

- **API REST**: Endpoints para execução e consulta de comandos
- **PostgreSQL**: Armazenamento persistente com tabela "newtable"
- **CORS**: Configurado para permitir requisições de frontend
- **Logging**: Registro automático de todas as execuções
- **Segurança**: Validação de inputs e tratamento de erros

## 📋 Endpoints

### GET `/`
Informações da API e endpoints disponíveis.

### POST `/executar`
Executa um comando no sistema.

**Request:**
```json
{
  "comando": "ipconfig"
}
```

**Response:**
```json
{
  "status": "sucesso",
  "comando": "ipconfig",
  "saida": "Configuração de IP do Windows...",
  "timestamp": "2026-03-16T20:51:54"
}
```

### GET `/historico`
Retorna os últimos comandos executados.

**Response:**
```json
{
  "comandos": [
    {
      "id": 12,
      "comando": "ipconfig",
      "saida_completa": "Configuração de IP...",
      "timestamp": "2026-03-16T20:51:54",
      "status": "sucesso"
    }
  ]
}
```

### GET `/api/comandos`
Lista todos os comandos do banco de dados.

### GET `/.well-known/appspecific/com.chrome.devtools.json`
Endpoint para evitar 404 do Chrome DevTools.

## 🛠️ Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` com suas configurações PostgreSQL:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
TABLE_NAME=newtable
```

### 2. Dependências

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Banco de Dados

O sistema criará automaticamente a tabela "newtable" no PostgreSQL na primeira execução.

## 🚀 Execução

### Desenvolvimento

```bash
python web_app.py
```

A API estará disponível em `http://localhost:8000`

### Produção

```bash
uvicorn web_app:app --host 0.0.0.0 --port 8000
```

## 📊 Estrutura do Projeto

```
back-endpython/
├── web_app.py              # Aplicação FastAPI principal
├── models_postgres.py      # Camada de dados PostgreSQL
├── models.py               # Modelo SQLite (legado)
├── entidades.py            # Entidades SQLAlchemy
├── requirements.txt        # Dependências Python
├── .env                    # Configurações (não versionado)
├── .env.example           # Exemplo de configurações
└── README.md              # Este arquivo
```

## � Configuração CORS

Para produção, configure origens específicas:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

## �️ Banco de Dados

### Tabela: newtable

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | SERIAL | Chave primária |
| comando | VARCHAR(500) | Comando executado |
| saida_completa | TEXT | Saída completa |
| timestamp | TIMESTAMP | Data/hora da execução |
| status | VARCHAR(50) | Status (sucesso/erro) |

## � Troubleshooting

### Erro de Conexão PostgreSQL
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no `.env`
- Verifique se o banco existe

### Comandos Não Executam
- Verifique permissões do sistema
- Confirme se o comando é válido
- Verifique logs de erro

### CORS Issues
- Configure origens permitidas
- Verifique se o frontend está na lista allow_origins

## 🔒 Segurança

- **Input Validation**: Validação de comandos
- **Error Handling**: Tratamento seguro de erros
- **CORS**: Restrição de origens em produção
- **SQL Injection**: Uso de parâmetros seguros

## 📝 Logs

A API registra automaticamente:
- Todas as execuções de comandos
- Erros e exceções
- Informações de conexão

## 🚀 Deploy

### Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku/Render

Configure as variáveis de ambiente no painel e faça deploy do código.

## 📞 Suporte

Para problemas:
1. Verifique os logs da aplicação
2. Teste os endpoints com Postman/curl
3. Confirme a configuração do banco de dados

## 📄 Licença

MIT License - livre para uso comercial e pessoal.
