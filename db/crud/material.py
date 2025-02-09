from sqlite3 import IntegrityError
from typing import Optional, List
from ..models import Material
from sqlalchemy.orm import Session
from db import get_db_auth

def create_material(nome: str, preco: float, quantidade: int, quantidade_minima: Optional[int] = None, local: Optional[str] = None) -> Material:
    db = get_db_auth()
    try:
        db_material = Material(nome=nome, preco=preco, quantidade=quantidade, quantidade_minima=quantidade_minima, local=local)
        db.add(db_material)
        db.commit()
        db.refresh(db_material)
        return db_material
    except IntegrityError:
        db.rollback()
        raise ValueError("Erro ao criar material. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao criar material: {str(e)}")
    finally:
        db.close()

def get_material(material_id: int) -> Optional[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).filter(Material.id == material_id).first()
    finally:
        db.close()

def get_material_by_nome(nome: str) -> Optional[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).filter(Material.nome == nome).first()
    finally:
        db.close()

def get_materiais(skip: int = 0, limit: int = 100) -> List[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).offset(skip).limit(limit).all()
    finally:
        db.close()

def update_material(material_id: int, nome: Optional[str] = None, preco: Optional[float] = None, 
                    quantidade: Optional[int] = None, quantidade_minima: Optional[int] = None, 
                    local: Optional[str] = None) -> Optional[Material]:
    db = get_db_auth()
    try:
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
    except IntegrityError:
        db.rollback()
        raise ValueError("Erro ao atualizar material. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao atualizar material: {str(e)}")
    finally:
        db.close()

def delete_material(material_id: int) -> bool:
    db = get_db_auth()
    try:
        db_material = db.query(Material).filter(Material.id == material_id).first()
        if db_material:
            db.delete(db_material)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao deletar material: {str(e)}")
    finally:
        db.close()