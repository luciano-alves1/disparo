import asyncio
from teste import executar_cmd_oculto_async

async def enviar_comando_para_api(comando):
    """Envia um comando para a API e retorna o resultado"""
    print(f"🚀 Enviando comando: {comando}")
    resultado = await executar_cmd_oculto_async(comando, aguardar_final=True)
    print(f"✅ Resultado: {resultado['status']}")
    return resultado

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Pega o comando da linha de comando
        comando = " ".join(sys.argv[1:])
        asyncio.run(enviar_comando_para_api(comando))
    else:
        print("Uso: python enviar_comando.py <comando>")
        print("Exemplos:")
        print("  python enviar_comando.py ipconfig")
        print("  python enviar_comando.py ping google.com -n 2")
        print("  python enviar_comando.py dir C:\\")
