from sqlalchemy.exc import IntegrityError
from ..models import Cliente
from typing import List, Optional

def create_cliente(db, nome: str, endereco: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> Cliente:
    existing_cliente = get_cliente_by_email(db, email)
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

def get_cliente(db, cliente_id: int) -> Optional[Cliente]:
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def get_cliente_by_email(db, email: str) -> Optional[Cliente]:
    return db.query(Cliente).filter(Cliente.email == email).first()

def get_cliente_by_filters(db, nome: Optional[str] = None, endereco: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> Optional[Cliente]:
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

def get_all_clientes(db) -> List[Cliente]:
    return db.query(Cliente).all()

def update_cliente(db, cliente_id: int, nome: Optional[str] = None, endereco: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> Optional[Cliente]:
    cliente = get_cliente(db, cliente_id)
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

def delete_cliente(db, cliente_id: int) -> bool:
    cliente = get_cliente(db, cliente_id)
    if cliente:
        db.delete(cliente)
        db.commit()
        return True
    return False