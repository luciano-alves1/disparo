import asyncio
from teste import executar_cmd_oculto_async, iniciar_servidor

async def testar_comandos_async():
    """Testa os comandos assíncronos"""
    print("🚀 Iniciando testes de comandos assíncronos...")
    
    # Teste 1: ipconfig
    print("\n📡 Testando ipconfig...")
    resultado1 = await executar_cmd_oculto_async("ipconfig", aguardar_final=True)
    print(f"Resultado ipconfig: {resultado1['status']}")
    
    # Teste 2: ping
    print("\n📡 Testando ping...")
    resultado2 = await executar_cmd_oculto_async("ping google.com -n 2", aguardar_final=True)
    print(f"Resultado ping: {resultado2['status']}")
    
    # Teste 3: background
    print("\n📡 Testando comando em background...")
    resultado3 = await executar_cmd_oculto_async("echo teste", aguardar_final=False)
    print(f"Resultado background: {resultado3['status']}")

if __name__ == "__main__":
    # Para usar: 
    # 1. Inicie o servidor em um terminal: python teste_async.py servidor
    # 2. Em outro terminal, execute os testes: python teste_async.py
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "servidor":
        print("🌐 Iniciando servidor FastAPI...")
        print("📍 API disponível em: http://localhost:8000")
        print("📍 Documentação em: http://localhost:8000/docs")
        iniciar_servidor()
    else:
        # Roda os testes (precisa do servidor rodando)
        asyncio.run(testar_comandos_async())
