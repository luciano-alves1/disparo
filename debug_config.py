#!/usr/bin/env python3
"""
Teste simples para verificar configuração
"""

import os
from dotenv import load_dotenv

print("🔍 Verificando configuração atual...")

# Tenta carregar do .env
try:
    load_dotenv('.env')
    print("✅ .env carregado")
except Exception as e:
    print(f"❌ Erro ao carregar .env: {e}")

# Mostra variáveis de ambiente
print(f"\n📋 Variáveis atuais:")
print(f"   DB_HOST: {os.getenv('DB_HOST', 'NÃO DEFINIDO')}")
print(f"   DB_PORT: {os.getenv('DB_PORT', 'NÃO DEFINIDO')}")
print(f"   DB_NAME: {os.getenv('DB_NAME', 'NÃO DEFINIDO')}")
print(f"   DB_USER: {os.getenv('DB_USER', 'NÃO DEFINIDO')}")
print(f"   DB_PASSWORD: {'***' if os.getenv('DB_PASSWORD') else 'NÃO DEFINIDO'}")
print(f"   TABLE_NAME: {os.getenv('TABLE_NAME', 'NÃO DEFINIDO')}")

print(f"\n⚠️  ATENÇÃO: Você precisa editar o arquivo .env com suas credenciais reais do PostgreSQL!")
