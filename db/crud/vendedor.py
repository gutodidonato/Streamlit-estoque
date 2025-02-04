from sqlalchemy.orm import Session
from ..models import Vendedor

# CRUD para Vendedor

def create_vendedor(db: Session, nome: str, vendas: int = 0):
    db_vendedor = Vendedor(nome=nome, vendas=vendas)
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def get_vendedor(db: Session, vendedor_id: int):
    return db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()

def get_vendedor_by_nome(db: Session, nome: str):
    return db.query(Vendedor).filter(Vendedor.nome == nome).first()

def get_vendedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vendedor).offset(skip).limit(limit).all()

def update_vendedor(db: Session, vendedor_id: int, nome: str = None, vendas: int = None):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    if db_vendedor:
        if nome:
            db_vendedor.nome = nome
        if vendas is not None:
            db_vendedor.vendas = vendas
        db.commit()
        db.refresh(db_vendedor)
    return db_vendedor

def delete_vendedor(db: Session, vendedor_id: int):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    if db_vendedor:
        db.delete(db_vendedor)
        db.commit()
        return True
    return False

def increment_vendas(db: Session, vendedor_id: int, increment: int = 1):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    if db_vendedor:
        db_vendedor.vendas += increment
        db.commit()
        db.refresh(db_vendedor)
    return db_vendedor