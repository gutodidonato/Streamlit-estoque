from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    senha = Column(String)
    email = Column(String)
    
    # Relacionamento com Vendas
    vendas_realizadas = relationship("Venda", back_populates="user")