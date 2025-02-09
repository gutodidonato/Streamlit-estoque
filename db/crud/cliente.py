from sqlalchemy.exc import IntegrityError
from ..models import Cliente
from typing import List, Optional
from db import get_db_auth

def create_cliente(nome: str, endereco: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> Cliente:
    db = get_db_auth()
    try:
        existing_cliente = get_cliente_by_email(email)
        if existing_cliente:
            raise ValueError("Cliente com este email já está cadastrado")
        cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone, email=email)
        try:
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            return cliente
        except IntegrityError:
            db.rollback()
            raise ValueError("Erro ao criar cliente. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao criar cliente: {str(e)}")
    finally:
        db.close()
        

def get_cliente(cliente_id: int) -> Optional[Cliente]:
    db = get_db_auth()
    try:
        return db.query(Cliente).filter(Cliente.id == cliente_id).first()
    finally:
        db.close()

def get_cliente_by_email(email: str) -> Optional[Cliente]:
    db = get_db_auth()
    try:
        return db.query(Cliente).filter(Cliente.email == email).first()
    finally:
        db.close()

def get_cliente_by_filters(nome: Optional[str] = None, endereco: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> Optional[Cliente]:
    db = get_db_auth()
    try:
        query = db.query(Cliente)
        if nome:
            query = query.filter(Cliente.nome == nome)
        if endereco:
            query = query.filter(Cliente.endereco == endereco)
        if telefone:
            query = query.filter(Cliente.telefone == telefone)
        if email:
            query = query.filter(Cliente.email == email)
        return query.first()
    finally:
        db.close()

def get_all_clientes() -> List[Cliente]:
    db = get_db_auth()
    try:
        return db.query(Cliente).all()
    finally:
        db.close()

def update_cliente(cliente_id: int, nome: Optional[str] = None, endereco: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> Optional[Cliente]:
    db = get_db_auth()
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            if nome:
                cliente.nome = nome
            if endereco:
                cliente.endereco = endereco
            if telefone:
                cliente.telefone = telefone
            if email:
                cliente.email = email
            db.commit()
            db.refresh(cliente)
            return cliente
        return None
    finally:
        db.close()

def delete_cliente(cliente_id: int) -> bool:
    db = get_db_auth()
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            db.delete(cliente)
            db.commit()
            return True
        return False
    finally:
        db.close()