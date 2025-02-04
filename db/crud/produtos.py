from ..models import Produto
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_produto(db: Session, nome: str, preco_atual: float, estoque: int, preco_aquisicao: float = None, categoria: str = None):
    db_produto = Produto(nome=nome, preco_atual=preco_atual, estoque=estoque, preco_aquisicao=preco_aquisicao, categoria=categoria)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def get_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()

def get_produto_by_nome(db: Session, nome: str):
    return db.query(Produto).filter(Produto.nome == nome).first()

def get_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).offset(skip).limit(limit).all()

def update_produto(db: Session, produto_id: int, nome: str = None, preco_atual: float = None, estoque: int = None, preco_aquisicao: float = None, categoria: str = None):
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
        db.commit()
        db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
        return True
    return False