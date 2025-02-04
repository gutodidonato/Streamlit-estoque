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
    
    # Relacionamento com Vendedor
    vendedor_id = Column(Integer, ForeignKey('vendedor.id'), nullable=False)
    vendedor = relationship("Vendedor", back_populates="vendas_realizadas")
    
    # Relacionamento com User
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="vendas_realizadas")
    
    # Relacionamento com Cliente (opcional)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=True)
    cliente = relationship("Cliente")
    