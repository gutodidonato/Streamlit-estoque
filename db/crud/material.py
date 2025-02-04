from ..models import Material
from sqlalchemy.orm import Session

def create_material(db: Session, nome: str, preco: float, quantidade: int, quantidade_minima: int = None, local: str = None):
    db_material = Material(nome=nome, preco=preco, quantidade=quantidade, quantidade_minima=quantidade_minima, local=local)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def get_material(db: Session, material_id: int):
    return db.query(Material).filter(Material.id == material_id).first()

def get_material_by_nome(db: Session, nome: str):
    return db.query(Material).filter(Material.nome == nome).first()

def get_materiais(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Material).offset(skip).limit(limit).all()

def update_material(db: Session, material_id: int, nome: str = None, preco: float = None, quantidade: int = None, quantidade_minima: int = None, local: str = None):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if db_material:
        if nome:
            db_material.nome = nome
        if preco is not None:
            db_material.preco = preco
        if quantidade is not None:
            db_material.quantidade = quantidade
        if quantidade_minima is not None:
            db_material.quantidade_minima = quantidade_minima
        if local:
            db_material.local = local
        db.commit()
        db.refresh(db_material)
    return db_material

def delete_material(db: Session, material_id: int):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if db_material:
        db.delete(db_material)
        db.commit()
        return True
    return False