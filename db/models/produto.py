from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco_atual = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    estoque_minimo = Column(Integer, nullable=True)
    estoque_alerta = Column(Integer, nullable=True)
    estoque_maximo = Column(Integer, nullable=True)
    preco_aquisicao = Column(Float, nullable=True)
    categoria = Column(String)
    local = Column(String, nullable=True)
    
    materiais = relationship("MaterialProduto", back_populates="produto")
    
    # Relacionamento com ItemCarrinho
    vendas = relationship("ItemCarrinho", back_populates="produto")
    
    