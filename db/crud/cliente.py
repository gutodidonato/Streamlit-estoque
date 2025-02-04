from sqlalchemy.exc import IntegrityError
from ..models import Cliente

def create_cliente(db, nome, endereco=None, telefone=None, email=None) -> object | None:
    '''
        Essa função cria um cliente, e caso tenha o mesmo email, invalida
    '''
    cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone, email=email)
    if not select_cliente(db, email=email):
        raise ValueError("Cliente com email já cadastrado")
    try:
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except IntegrityError:
        db.rollback()
        raise ValueError("Cliente já existe")

def select_cliente_id(db, id) -> Cliente | None:
    return db.query(Cliente).filter(Cliente.id == id).first()

def select_cliente(db, nome=None, endereco=None, telefone=None, email=None) -> Cliente | None:
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

def select_cliente_all(db) -> list[Cliente]:
    return db.query(Cliente).all()

def update_cliente(db, cliente_id, nome=None, endereco=None, telefone=None, email=None) -> Cliente | None:
    cliente = select_cliente_id(db, cliente_id)
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

def delete_cliente(db, cliente_id) -> bool:
    cliente = select_cliente_id(db, cliente_id)
    if cliente:
        db.delete(cliente)
        db.commit()
        return True
    return False
