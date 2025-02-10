from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..db import Base

class Material(Base):
    __tablename__ = 'material'
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
    
    produtos = relationship("MaterialProduto", back_populates="material")
    
class MaterialProduto(Base):
    __tablename__ = 'material_produto'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produto.id'))
    material_id = Column(Integer, ForeignKey('material.id')) 
    
    produto = relationship("Produto", back_populates="materiais")
    material = relationship("Material", back_populates="produtos")