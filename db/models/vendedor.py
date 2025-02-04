from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class Vendedor(Base):
    __tablename__ = 'vendedor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    vendas = Column(Integer)
    
    # Relacionamento com Venda
    vendas_realizadas = relationship("Venda", back_populates="vendedor")