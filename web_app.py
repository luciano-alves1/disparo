from models_postgres import init_db, salvar_comando, buscar_historico, listar_todos_comandos
import subprocess
import asyncio
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI(title="Executor de Comandos API", description="API para execução de comandos do sistema")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite acesso de qualquer origem na rede
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def executar_cmd_oculto(comando_cmd):
    """Executa comando e retorna a saída"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    
    comando = f'cmd.exe /c {comando_cmd}'
    
    try:
        processo = subprocess.Popen(
            comando,
            shell=True,
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='cp850'
        )
        
        stdout, stderr = processo.communicate(timeout=30)
        
        if stdout:
            return stdout
        elif stderr:
            return f"ERRO: {stderr}"
        else:
            return "Comando executado sem saída"
            
    except Exception as e:
        return f"ERRO: {str(e)}"


@app.get("/")
async def root():
    """API Root - Endpoint de verificação"""
    return {
        "message": "API Executor de Comandos",
        "version": "1.0.0",
        "endpoints": {
            "executar": "POST /executar - Executa comandos",
            "historico": "GET /historico - Retorna histórico",
            "comandos": "GET /api/comandos - Lista todos os comandos"
        }
    }

@app.post("/executar")
async def executar_comando_api(request: Request):
    """API para executar comando"""
    data = await request.json()
    comando = data.get('comando', '')
    client_ip = request.client.host
    client_info = f"Cliente: {client_ip}"
    
    if not comando:
        return {"status": "erro", "erro": "Comando não fornecido"}
    
    # Para comandos de rede, retorna informações do cliente
    if comando.lower() in ['ipconfig', 'ifconfig', 'ip addr', 'hostname']:
        saida = f"Informações do cliente {client_ip}:\n"
        saida += f"IP de acesso: {client_ip}\n"
        saida += f"User-Agent: {request.headers.get('user-agent', 'N/A')}\n"
        saida += f"Data/Hora: {datetime.now().isoformat()}\n"
        
        # Se for acesso local, executa o comando real
        if client_ip in ['127.0.0.1', 'localhost', '::1']:
            saida_real = executar_cmd_oculto(comando)
            saida += f"\n\n--- Saída local ---\n{saida_real}"
        
        # Salva no banco
        salvar_comando(comando, saida, "sucesso")
        
        return {
            "status": "sucesso",
            "comando": comando,
            "saida": saida,
            "timestamp": datetime.now().isoformat(),
            "client_info": client_info
        }
    
    # Para outros comandos, executa normalmente no servidor
    saida = executar_cmd_oculto(comando)
    
    # Salva no banco
    salvar_comando(comando, saida, "sucesso")
    
    return {
        "status": "sucesso",
        "comando": comando,
        "saida": saida,
        "timestamp": datetime.now().isoformat(),
        "client_info": client_info
    }

@app.get("/historico")
async def get_historico():
    """Retorna o histórico de comandos"""
    comandos = buscar_historico(10)
    
    return {"comandos": comandos}

@app.get("/api/comandos")
async def listar_todos_comandos():
    """Lista todos os comandos do banco"""
    return listar_todos_comandos()

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    """Chrome DevTools endpoint - returns empty to prevent 404"""
    return {}

if __name__ == "__main__":
    # Inicializa o banco de dados
    init_db()
    
    # Inicia o servidor
    import uvicorn
    print("🌐 Servidor iniciado em: http://localhost:8000")
    print("💾 Banco de dados: PostgreSQL")
    uvicorn.run(app, host="0.0.0.0", port=8000)

