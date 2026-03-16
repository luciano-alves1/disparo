import subprocess
import time
import asyncio
import aiohttp
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def executar_cmd_oculto(comando_cmd, aguardar_final=False):
    """
    Executa qualquer comando no CMD sem mostrar janela
    
    Args:
        comando_cmd (str): Comando a ser executado (ex: 'dir C:\\')
        aguardar_final (bool): Se True, espera o comando terminar
    
    Returns:
        str: Saída do comando (se aguardar_final=True)
    """
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    
    # Comando completo para CMD
    comando = f'cmd.exe /c {comando_cmd}'
    
    try:
        if aguardar_final:
            # Aguarda o término e captura a saída
            processo = subprocess.Popen(
                comando,
                shell=True,
                startupinfo=startupinfo,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='cp850'  # Encoding do CMD no Windows
            )
            
            stdout, stderr = processo.communicate(timeout=30)
            
            if stdout:
                print(f"📤 Saída do comando:\n{stdout}")
            if stderr:
                print(f"⚠️ Erro: {stderr}")
                
            return stdout
            
        else:
            # Apenas executa e continua (não espera)
            subprocess.Popen(
                comando,
                shell=True,
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Comando executado em background: {comando_cmd}")
            return None
            
    except subprocess.TimeoutExpired:
        processo.kill()
        print("⏰ Tempo limite excedido")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

# Modelo de dados para a API
class ComandoResultado(BaseModel):
    comando: str
    saida: str
    timestamp: str
    status: str
    erro: str = None

# Servidor FastAPI
app = FastAPI(title="Comando Assíncrono API")

# Armazenamento temporário dos dados recebidos
dados_recebidos_lista = []

@app.post("/api/comando")
async def receber_dados(dados: ComandoResultado):
    """Recebe dados de comando executado assincronamente"""
    print(f"📥 Dados recebidos: {dados.comando}")
    print(f"📤 Saída: {dados.saida[:100]}...")
    
    # Armazena para visualização posterior
    dados_recebidos_lista.append({
        "comando": dados.comando,
        "saida": dados.saida,
        "timestamp": dados.timestamp,
        "status": dados.status,
        "erro": dados.erro
    })
    
    # Retorna os dados completos recebidos para visualização
    return {
        "status": "recebido", 
        "timestamp": dados.timestamp,
        "dados_recebidos": {
            "comando": dados.comando,
            "saida": dados.saida,
            "status": dados.status,
            "erro": dados.erro
        }
    }

@app.get("/api/comando")
async def listar_comandos():
    """Lista todos os comandos recebidos"""
    return {
        "total": len(dados_recebidos_lista),
        "comandos": dados_recebidos_lista
    }

@app.get("/")
async def root():
    return {"message": "API de Comandos Assíncronos"}

# Função assíncrona que executa comando e envia para rota
async def executar_cmd_oculto_async(comando_cmd, aguardar_final=False, url_rota="http://localhost:8000/api/comando"):
    """
    Executa comando de forma assíncrona e envia resultado para rota
    
    Args:
        comando_cmd (str): Comando a ser executado
        aguardar_final (bool): Se True, espera o comando terminar
        url_rota (str): URL da rota para enviar os dados
    
    Returns:
        dict: Resultado da execução e envio
    """
    if not aguardar_final:
        # Executa em background sem esperar
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: executar_cmd_oculto(comando_cmd, False))
        return {"status": "executado_background", "comando": comando_cmd}
    
    # Executa e espera resultado
    loop = asyncio.get_event_loop()
    saida = await loop.run_in_executor(None, lambda: executar_cmd_oculto(comando_cmd, True))
    
    # Prepara dados para envio
    dados = {
        "comando": comando_cmd,
        "saida": saida or "",
        "timestamp": datetime.now().isoformat(),
        "status": "sucesso" if saida else "erro"
    }
    
    # Envia para rota de forma assíncrona
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url_rota, json=dados) as response:
                if response.status == 200:
                    resultado_envio = await response.json()
                    print(f" Dados enviados com sucesso: {resultado_envio}")
                    return {"status": "enviado", "dados": dados, "resposta": resultado_envio}
                else:
                    print(f" Erro ao enviar dados: {response.status}")
                    return {"status": "erro_envio", "dados": dados}
    except Exception as e:
        print(f" Erro na requisição: {e}")
        return {"status": "erro_requisicao", "dados": dados, "erro": str(e)}

# Função para iniciar servidor
def iniciar_servidor():
    """Inicia o servidor FastAPI"""
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

# Exemplos de uso assíncrono
async def exemplos_uso_async():
    """Exemplos de como usar a função assíncrona"""
    
    # Exemplo 1: Executar e enviar resultado
    resultado = await executar_cmd_oculto_async("ipconfig", aguardar_final=True)
    print(f"Resultado: {resultado}")
    
    # Exemplo 2: Executar em background
    resultado_bg = await executar_cmd_oculto_async("start chrome.exe", aguardar_final=False)
    print(f"Background: {resultado_bg}")

# Exemplos de uso síncrono (comentados para não executar automaticamente)
# executar_cmd_oculto("start chrome.exe")  # Abre Chrome
# executar_cmd_oculto("ipconfig", aguardar_final=True)  # Executa e mostra resultado
# executar_cmd_oculto("ping google.com", aguardar_final=True)  # Ping e mostra resultado