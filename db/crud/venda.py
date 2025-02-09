from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional
from db import get_db_auth
from ..models import Venda, ItemVenda, Vendedor, User, Cliente, Produto

def create_venda(vendedor_id: int, user_id: int, cliente_id: Optional[int], frete: float) -> Optional[Venda]:
    db = get_db_auth()
    try:
        nova_venda = Venda(
            vendedor_id=vendedor_id,
            user_id=user_id,
            cliente_id=cliente_id,
            frete=frete,
            total=frete
        )
        db.add(nova_venda)
        db.commit()
        db.refresh(nova_venda)
        return nova_venda
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao criar venda: {str(e)}")
        return None
    finally:
        db.close()

def get_venda(venda_id: int) -> Optional[Venda]:
    db = get_db_auth()
    try:
        return db.query(Venda).filter(Venda.id == venda_id).first()
    finally:
        db.close()

def get_vendas(skip: int = 0, limit: int = 100) -> List[Venda]:
    db = get_db_auth()
    try:
        return db.query(Venda).offset(skip).limit(limit).all()
    finally:
        db.close()

def get_vendas_by_cliente(cliente_id: int) -> List[Venda]:
    db = get_db_auth()
    try:
        return db.query(Venda).filter(Venda.cliente_id == cliente_id).all()
    finally:
        db.close()

def get_vendas_by_vendedor(vendedor_id: int) -> List[Venda]:
    db = get_db_auth()
    try:
        return db.query(Venda).filter(Venda.vendedor_id == vendedor_id).all()
    finally:
        db.close()

def get_vendas_by_user(user_id: int) -> List[Venda]:
    db = get_db_auth()
    try:
        return db.query(Venda).filter(Venda.user_id == user_id).all()
    finally:
        db.close()

def update_venda(venda_id: int, frete: Optional[float] = None, confirmar: Optional[bool] = None) -> Optional[Venda]:
    db = get_db_auth()
    try:
        venda = db.query(Venda).filter(Venda.id == venda_id).first()
        if venda:
            if frete is not None:
                venda.frete = frete
            if confirmar is not None:
                venda.confirmar = confirmar
            venda.total = calcular_total_venda(venda_id)
            db.commit()
            db.refresh(venda)
            return venda
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao atualizar venda: {str(e)}")
        return None
    finally:
        db.close()

def delete_venda(venda_id: int) -> bool:
    db = get_db_auth()
    try:
        venda = db.query(Venda).filter(Venda.id == venda_id).first()
        if venda:
            db.delete(venda)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao deletar venda: {str(e)}")
        return False
    finally:
        db.close()

# Funções para ItemVenda

def add_item_to_venda(venda_id: int, produto_id: int, quantidade: int) -> Optional[ItemVenda]:
    db = get_db_auth()
    try:
        venda = db.query(Venda).get(venda_id)
        produto = db.query(Produto).get(produto_id)
        if not venda or not produto:
            return None
        
        novo_item = ItemVenda(venda_id=venda_id, produto_id=produto_id, quantidade=quantidade, preco_unitario=produto.preco_atual)
        db.add(novo_item)
        venda.total = calcular_total_venda(venda_id)
        db.commit()
        db.refresh(novo_item)
        return novo_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao adicionar item à venda: {str(e)}")
        return None
    finally:
        db.close()

def remove_item_from_venda(venda_id: int, item_id: int) -> bool:
    db = get_db_auth()
    try:
        item = db.query(ItemVenda).filter(ItemVenda.id == item_id, ItemVenda.venda_id == venda_id).first()
        if item:
            db.delete(item)
            venda = db.query(Venda).get(venda_id)
            venda.total = calcular_total_venda(venda_id)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao remover item da venda: {str(e)}")
        return False
    finally:
        db.close()

def update_item_venda(item_id: int, quantidade: Optional[int] = None) -> Optional[ItemVenda]:
    db = get_db_auth()
    try:
        item = db.query(ItemVenda).get(item_id)
        if item:
            if quantidade is not None:
                item.quantidade = quantidade
            venda = db.query(Venda).get(item.venda_id)
            venda.total = calcular_total_venda(item.venda_id)
            db.commit()
            db.refresh(item)
            return item
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao atualizar item da venda: {str(e)}")
        return None
    finally:
        db.close()

def get_itens_venda(venda_id: int) -> List[ItemVenda]:
    db = get_db_auth()
    try:
        return db.query(ItemVenda).filter(ItemVenda.venda_id == venda_id).all()
    finally:
        db.close()

# Funções auxiliares

def calcular_total_venda(venda_id: int) -> float:
    db = get_db_auth()
    try:
        venda = db.query(Venda).get(venda_id)
        if venda:
            total_itens = sum(item.quantidade * item.preco_unitario for item in venda.itens)
            return total_itens + venda.frete
        return 0.0
    finally:
        db.close()

def confirmar_venda(venda_id: int) -> Optional[Venda]:
    db = get_db_auth()
    try:
        venda = db.query(Venda).get(venda_id)
        if venda and not venda.confirmar:
            venda.confirmar = True
            venda.total = calcular_total_venda(venda_id)
            db.commit()
            db.refresh(venda)
            return venda
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao confirmar venda: {str(e)}")
        return None
    finally:
        db.close()