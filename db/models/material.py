from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from ..db import Base

class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    quantidade_minima = Column(Integer, nullable=True)
    local = Column(String)
    