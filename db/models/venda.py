from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db import Base
from datetime import datetime

class Venda(Base):
    __tablename__ = 'venda'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, default=datetime.utcnow)
    frete = Column(Float)
    total = Column(Float, nullable=False)
    confirmar = Column(Boolean, default=False)
    
    vendedor_id = Column(Integer, ForeignKey('vendedor.id'), nullable=False)
    vendedor = relationship("Vendedor", back_populates="vendas_realizadas")
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="vendas_realizadas")
    
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=True)
    cliente = relationship("Cliente", back_populates="compras")
    
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

    
    
class ItemVenda(Base):
    __tablename__ = 'item_venda'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venda_id = Column(Integer, ForeignKey('venda.id'))
    produto_id = Column(Integer, ForeignKey('produto.id'))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    
    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto")