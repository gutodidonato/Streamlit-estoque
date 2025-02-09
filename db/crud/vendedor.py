from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db import get_db_auth
from ..models import Vendedor

# CRUD para Vendedor

def create_vendedor(nome: str, vendas: int = 0) -> Optional[Vendedor]:
    db = get_db_auth()
    try:
        db_vendedor = Vendedor(nome=nome, vendas=vendas)
        db.add(db_vendedor)
        db.commit()
        db.refresh(db_vendedor)
        return db_vendedor
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao criar vendedor: {str(e)}")
        return None
    finally:
        db.close()

def get_vendedor(vendedor_id: int) -> Optional[Vendedor]:
    db = get_db_auth()
    try:
        return db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    finally:
        db.close()

def get_vendedor_by_nome(nome: str) -> Optional[Vendedor]:
    db = get_db_auth()
    try:
        return db.query(Vendedor).filter(Vendedor.nome == nome).first()
    finally:
        db.close()

def get_vendedores(skip: int = 0, limit: int = 100) -> List[Vendedor]:
    db = get_db_auth()
    try:
        return db.query(Vendedor).offset(skip).limit(limit).all()
    finally:
        db.close()

def update_vendedor(vendedor_id: int, nome: Optional[str] = None, vendas: Optional[int] = None) -> Optional[Vendedor]:
    db = get_db_auth()
    try:
        db_vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        if db_vendedor:
            if nome:
                db_vendedor.nome = nome
            if vendas is not None:
                db_vendedor.vendas = vendas
            db.commit()
            db.refresh(db_vendedor)
        return db_vendedor
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao atualizar vendedor: {str(e)}")
        return None
    finally:
        db.close()

def delete_vendedor(vendedor_id: int) -> bool:
    db = get_db_auth()
    try:
        db_vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        if db_vendedor:
            db.delete(db_vendedor)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao deletar vendedor: {str(e)}")
        return False
    finally:
        db.close()

def increment_vendas(vendedor_id: int, increment: int = 1) -> Optional[Vendedor]:
    db = get_db_auth()
    try:
        db_vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        if db_vendedor:
            db_vendedor.vendas += increment
            db.commit()
            db.refresh(db_vendedor)
        return db_vendedor
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao incrementar vendas do vendedor: {str(e)}")
        return None
    finally:
        db.close()