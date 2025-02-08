from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional
from ..models import Venda, ItemVenda, Vendedor, User, Cliente, Produto

def create_venda(db: Session, vendedor_id: int, user_id: int, cliente_id: Optional[int], frete: float) -> Optional[Venda]:
    nova_venda = Venda(
        vendedor_id=vendedor_id,
        user_id=user_id,
        cliente_id=cliente_id,
        frete=frete,
        total=frete  
    )
    try:
        db.add(nova_venda)
        db.commit()
        db.refresh(nova_venda)
        return nova_venda
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao criar venda: {str(e)}")
        return None

def get_venda(db: Session, venda_id: int) -> Optional[Venda]:
    return db.query(Venda).filter(Venda.id == venda_id).first()

def get_vendas(db: Session, skip: int = 0, limit: int = 100) -> List[Venda]:
    return db.query(Venda).offset(skip).limit(limit).all()

def get_vendas_by_cliente(db: Session, cliente_id: int) -> List[Venda]:
    return db.query(Venda).filter(Venda.cliente_id == cliente_id).all()

def get_vendas_by_vendedor(db: Session, vendedor_id: int) -> List[Venda]:
    return db.query(Venda).filter(Venda.vendedor_id == vendedor_id).all()

def get_vendas_by_user(db: Session, user_id: int) -> List[Venda]:
    return db.query(Venda).filter(Venda.user_id == user_id).all()

def update_venda(db: Session, venda_id: int, frete: Optional[float] = None, confirmar: Optional[bool] = None) -> Optional[Venda]:
    venda = get_venda(db, venda_id)
    if venda:
        if frete is not None:
            venda.frete = frete
        if confirmar is not None:
            venda.confirmar = confirmar
        venda.total = calcular_total_venda(db, venda_id)
        try:
            db.commit()
            db.refresh(venda)
            return venda
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao atualizar venda: {str(e)}")
            return None
    return None

def delete_venda(db: Session, venda_id: int) -> bool:
    venda = get_venda(db, venda_id)
    if venda:
        try:
            db.delete(venda)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao deletar venda: {str(e)}")
            return False
    return False

# Funções para ItemVenda

def add_item_to_venda(db: Session, venda_id: int, produto_id: int, quantidade: int) -> Optional[ItemVenda]:
    venda = get_venda(db, venda_id)
    produto = db.query(Produto).get(produto_id)
    if not venda or not produto:
        return None
    
    novo_item = ItemVenda(venda_id=venda_id, produto_id=produto_id, quantidade=quantidade, preco_unitario=produto.preco_atual)
    try:
        db.add(novo_item)
        venda.total = calcular_total_venda(db, venda_id)
        db.commit()
        db.refresh(novo_item)
        return novo_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao adicionar item à venda: {str(e)}")
        return None

def remove_item_from_venda(db: Session, venda_id: int, item_id: int) -> bool:
    item = db.query(ItemVenda).filter(ItemVenda.id == item_id, ItemVenda.venda_id == venda_id).first()
    if item:
        try:
            db.delete(item)
            venda = get_venda(db, venda_id)
            venda.total = calcular_total_venda(db, venda_id)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao remover item da venda: {str(e)}")
            return False
    return False

def update_item_venda(db: Session, item_id: int, quantidade: Optional[int] = None) -> Optional[ItemVenda]:
    item = db.query(ItemVenda).get(item_id)
    if item:
        if quantidade is not None:
            item.quantidade = quantidade
        try:
            venda = get_venda(db, item.venda_id)
            venda.total = calcular_total_venda(db, item.venda_id)
            db.commit()
            db.refresh(item)
            return item
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao atualizar item da venda: {str(e)}")
            return None
    return None

def get_itens_venda(db: Session, venda_id: int) -> List[ItemVenda]:
    return db.query(ItemVenda).filter(ItemVenda.venda_id == venda_id).all()

# Funções auxiliares

def calcular_total_venda(db: Session, venda_id: int) -> float:
    venda = get_venda(db, venda_id)
    if venda:
        total_itens = sum(item.quantidade * item.preco_unitario for item in venda.itens)
        return total_itens + venda.frete
    return 0.0

def confirmar_venda(db: Session, venda_id: int) -> Optional[Venda]:
    venda = get_venda(db, venda_id)
    if venda and not venda.confirmar:
        venda.confirmar = True
        venda.total = calcular_total_venda(db, venda_id)
        try:
            db.commit()
            db.refresh(venda)
            return venda
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao confirmar venda: {str(e)}")
            return None
    return None