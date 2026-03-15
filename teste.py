import subprocess
import time
import asyncio
import aiohttp
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

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

# Exemplos de uso
executar_cmd_oculto("start chrome.exe")  # Abre Chrome
executar_cmd_oculto("ipconfig", aguardar_final=True)  # Executa e mostra resultado
executar_cmd_oculto("ping google.com", aguardar_final=True)  # Ping e mostra resultado