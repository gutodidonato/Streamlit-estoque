from typing import List, Optional
from db import get_db_auth
from ..models import Produto
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_produto(nome: str,
                   preco_atual: float,
                   estoque: int,
                   estoque_minimo: Optional[int] = None,
                   estoque_alerta: Optional[int] = None,
                   estoque_maximo: Optional[int] = None,
                   preco_aquisicao: Optional[float] = None,
                   categoria: Optional[str] = None,
                   local: Optional[str] = None
                   ) -> Produto:
    db = get_db_auth()
    try:
        db_produto = Produto(nome=nome,
                             preco_atual=preco_atual,
                             estoque=estoque,
                             estoque_minimo=estoque_minimo,
                             estoque_alerta=estoque_alerta,
                             estoque_maximo=estoque_maximo,
                             preco_aquisicao=preco_aquisicao,
                             categoria=categoria,
                             local=local)
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        return db_produto
    except IntegrityError:
        db.rollback()
        raise ValueError("Erro ao criar produto. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao criar produto: {str(e)}")
    finally:
        db.close()

def get_produto(produto_id: int) -> Optional[Produto]:
    db = get_db_auth()
    try:
        return db.query(Produto).filter(Produto.id == produto_id).first()
    finally:
        db.close()

def get_produto_by_nome(nome: str) -> Optional[Produto]:
    db = get_db_auth()
    try:
        return db.query(Produto).filter(Produto.nome == nome).first()
    finally:
        db.close()

def get_produtos(skip: int = 0, limit: int = 100) -> List[Produto]:
    db = get_db_auth()
    try:
        return db.query(Produto).offset(skip).limit(limit).all()
    finally:
        db.close()
        
def get_produtos_abaixo_minimo() -> List[Produto]:
    db = get_db_auth()
    try:
        return db.query(Produto).filter(Produto.estoque < Produto.estoque_minimo).all()
    finally:
        db.close()

def update_produto(produto_id: int,
                   nome: Optional[str] = None,
                   preco_atual: Optional[float] = None, 
                   estoque: Optional[int] = None,
                   estoque_minimo: Optional[int] = None,
                   estoque_alerta: Optional[int] = None,
                   estoque_maximo: Optional[int] = None,
                   preco_aquisicao: Optional[float] = None, 
                   categoria: Optional[str] = None,
                   local: Optional[str] = None
                   ) -> Optional[Produto]:
    db = get_db_auth()
    try:
        db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if db_produto:
            if nome:
                db_produto.nome = nome
            if preco_atual is not None:
                db_produto.preco_atual = preco_atual
            if estoque is not None:
                db_produto.estoque = estoque
            if preco_aquisicao is not None:
                db_produto.preco_aquisicao = preco_aquisicao
            if categoria:
                db_produto.categoria = categoria
            if estoque_minimo is not None:
                db_produto.estoque_minimo = estoque_minimo
            if estoque_alerta is not None:
                db_produto.estoque_alerta = estoque_alerta
            if estoque_maximo is not None:
                db_produto.estoque_maximo = estoque_maximo
            if local is not None:
                db_produto.local = local
            db.commit()
            db.refresh(db_produto)
        return db_produto
    except IntegrityError:
        db.rollback()
        raise ValueError("Erro ao atualizar produto. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao atualizar produto: {str(e)}")
    finally:
        db.close()

def delete_produto(produto_id: int) -> bool:
    db = get_db_auth()
    try:
        db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if db_produto:
            db.delete(db_produto)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao deletar produto: {str(e)}")
    finally:
        db.close()