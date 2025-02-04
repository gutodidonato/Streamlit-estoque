from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import ItemCarrinho, Carrinho, Produto, Cliente

# CRUD para ItemCarrinho

def create_item_carrinho(db: Session, carrinho_id: int, produto_id: int, quantidade: int) -> ItemCarrinho:
    item = ItemCarrinho(carrinho_id=carrinho_id, produto_id=produto_id, quantidade=quantidade)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item_carrinho(db: Session, item_id: int) -> Optional[ItemCarrinho]:
    return db.query(ItemCarrinho).filter(ItemCarrinho.id == item_id).first()

def get_itens_by_carrinho(db: Session, carrinho_id: int) -> List[ItemCarrinho]:
    return db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho_id).all()

def update_item_carrinho(db: Session, item_id: int, quantidade: int) -> Optional[ItemCarrinho]:
    item = get_item_carrinho(db, item_id)
    if item:
        item.quantidade = quantidade
        db.commit()
        db.refresh(item)
        return item
    return None

def delete_item_carrinho(db: Session, item_id: int) -> bool:
    item = get_item_carrinho(db, item_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

# CRUD para Carrinho

def create_carrinho(db: Session, cliente_id: int) -> Carrinho:
    carrinho = Carrinho(cliente_id=cliente_id)
    db.add(carrinho)
    db.commit()
    db.refresh(carrinho)
    return carrinho

def get_carrinho(db: Session, carrinho_id: int) -> Optional[Carrinho]:
    return db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()

def get_carrinho_by_cliente(db: Session, cliente_id: int) -> Optional[Carrinho]:
    return db.query(Carrinho).filter(Carrinho.cliente_id == cliente_id).first()

def get_all_carrinhos(db: Session) -> List[Carrinho]:
    return db.query(Carrinho).all()

def delete_carrinho(db: Session, carrinho_id: int) -> bool:
    carrinho = get_carrinho(db, carrinho_id)
    if carrinho:
        db.delete(carrinho)
        db.commit()
        return True
    return False

# Funções auxiliares

def add_item_to_carrinho(db: Session, cliente_id: int, produto_id: int, quantidade: int) -> Optional[ItemCarrinho]:
    carrinho = get_carrinho_by_cliente(db, cliente_id)
    if not carrinho:
        carrinho = create_carrinho(db, cliente_id)
    
    existing_item = db.query(ItemCarrinho).filter(
        ItemCarrinho.carrinho_id == carrinho.id,
        ItemCarrinho.produto_id == produto_id
    ).first()

    if existing_item:
        existing_item.quantidade += quantidade
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        return create_item_carrinho(db, carrinho.id, produto_id, quantidade)

def remove_item_from_carrinho(db: Session, cliente_id: int, produto_id: int) -> bool:
    carrinho = get_carrinho_by_cliente(db, cliente_id)
    if carrinho:
        item = db.query(ItemCarrinho).filter(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == produto_id
        ).first()
        if item:
            db.delete(item)
            db.commit()
            return True
    return False

def get_carrinho_total(db: Session, carrinho_id: int) -> float:
    itens = get_itens_by_carrinho(db, carrinho_id)
    total = 0.0
    for item in itens:
        produto = db.query(Produto).get(item.produto_id)
        if produto:
            total += produto.preco * item.quantidade
    return total

def clear_carrinho(db: Session, cliente_id: int) -> bool:
    carrinho = get_carrinho_by_cliente(db, cliente_id)
    if carrinho:
        db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho.id).delete()
        db.commit()
        return True
    return False