from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ComandoExecutado(Base):
    __tablename__ = "comandos_executados"
    
    id = Column(Integer, primary_key=True, index=True)
    comando = Column(String(500), nullable=False)
    saida_completa = Column(Text, nullable=False)  # Campo único para toda a saída
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="sucesso")