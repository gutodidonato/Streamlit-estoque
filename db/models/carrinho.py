from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class ItemCarrinho(Base):
    __tablename__ = 'item_carrinho'
    id = Column(Integer, primary_key=True)
    carrinho_id = Column(Integer, ForeignKey('carrinho.id'))
    produto_id = Column(Integer, ForeignKey('produto.id'))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)  
    
    carrinho = relationship("Carrinho", back_populates="itens")
    produto = relationship("Produto")

class Carrinho(Base):
    __tablename__ = 'carrinho'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    itens = relationship("ItemCarrinho", back_populates="carrinho", cascade="all, delete-orphan")
