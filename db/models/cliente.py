from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    endereco = Column(String)
    telefone = Column(String)
    email = Column(String)

    # Relacionamento com Venda
    compras = relationship("Venda", back_populates="cliente")
    carrinho = relationship("Carrinho", back_populates="cliente", uselist=False)
