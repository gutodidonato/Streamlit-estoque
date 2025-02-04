from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    endereco = Column(String)
    telefone = Column(String)
    email = Column(String)

    carrinhos = relationship("Carrinho")
    vendas = relationship("Venda")