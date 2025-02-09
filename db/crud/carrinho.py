from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db import get_db_auth
from typing import List, Optional
from ..models import ItemCarrinho, Carrinho, Produto, Cliente
from .produtos import get_produto

# CRUD para ItemCarrinho

def create_item_carrinho(carrinho_id: int, produto_id: int, quantidade: int) -> ItemCarrinho:
    db = get_db_auth()
    try:
        produto = get_produto(produto_id=produto_id)
        item = ItemCarrinho(carrinho_id=carrinho_id,
                            produto_id=produto_id,
                            quantidade=quantidade,
                            preco_unitario=produto.preco_atual)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except:
        db.rollback()
        raise IntegrityError
    finally:
        db.close()

def get_item_carrinho(item_id: int) -> Optional[ItemCarrinho]:
    db = get_db_auth()
    try:
        return db.query(ItemCarrinho).filter(ItemCarrinho.id == item_id).first()
    finally:
        db.close()

def get_itens_by_carrinho(carrinho_id: int) -> List[ItemCarrinho]:
    db = get_db_auth()
    try:
        return db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho_id).all()
    finally:
        db.close()

def update_item_carrinho(item_id: int, quantidade: int) -> Optional[ItemCarrinho]:
    db = get_db_auth()
    try:
        item = db.query(ItemCarrinho).filter(ItemCarrinho.id == item_id).first()
        if item:
            item.quantidade = quantidade
            db.commit()
            db.refresh(item)
            return item
        return None
    finally:
        db.close()

def delete_item_carrinho(item_id: int) -> bool:
    db = get_db_auth()
    try:
        item = db.query(ItemCarrinho).filter(ItemCarrinho.id == item_id).first()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False
    finally:
        db.close()

# CRUD para Carrinho

def create_carrinho(cliente_id: int) -> Carrinho:
    db = get_db_auth()
    try:
        carrinho = Carrinho(cliente_id=cliente_id)
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)
        return carrinho
    finally:
        db.close()

def get_carrinho(carrinho_id: int) -> Optional[Carrinho]:
    db = get_db_auth()
    try:
        return db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()
    finally:
        db.close()

def get_carrinho_by_cliente(cliente_id: int) -> Optional[Carrinho]:
    db = get_db_auth()
    try:
        return db.query(Carrinho).filter(Carrinho.cliente_id == cliente_id).first()
    finally:
        db.close()

def get_all_carrinhos() -> List[Carrinho]:
    db = get_db_auth()
    try:
        return db.query(Carrinho).all()
    finally:
        db.close()

def delete_carrinho(carrinho_id: int) -> bool:
    db = get_db_auth()
    try:
        carrinho = db.query(Carrinho).filter(Carrinho.id == carrinho_id).first()
        if carrinho:
            db.delete(carrinho)
            db.commit()
            return True
        return False
    finally:
        db.close()

# Funções auxiliares

def add_item_to_carrinho(cliente_id: int, produto_id: int, quantidade: int) -> Optional[ItemCarrinho]:
    db = get_db_auth()
    try:
        carrinho = db.query(Carrinho).filter(Carrinho.cliente_id == cliente_id).first()
        if not carrinho:
            carrinho = create_carrinho(cliente_id)
        
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
            return create_item_carrinho(carrinho.id, produto_id, quantidade)
    finally:
        db.close()

def remove_item_from_carrinho(cliente_id: int, produto_id: int) -> bool:
    db = get_db_auth()
    try:
        carrinho = db.query(Carrinho).filter(Carrinho.cliente_id == cliente_id).first()
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
    finally:
        db.close()

def get_carrinho_total(carrinho_id: int) -> float:
    db = get_db_auth()
    try:
        itens = db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho_id).all()
        total = 0.0
        for item in itens:
            produto = db.query(Produto).get(item.produto_id)
            if produto:
                total += produto.preco * item.quantidade
        return total
    finally:
        db.close()

def clear_carrinho(cliente_id: int) -> bool:
    db = get_db_auth()
    try:
        carrinho = db.query(Carrinho).filter(Carrinho.cliente_id == cliente_id).first()
        if carrinho:
            db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho.id).delete()
            db.commit()
            return True
        return False
    finally:
        db.close()