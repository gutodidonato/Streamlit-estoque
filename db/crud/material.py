from typing import List, Optional

from sqlalchemy import and_
from db import get_db_auth
from ..models import Material, Produto, MaterialProduto
from .produtos import get_produto
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_material(nome: str,
                    preco_atual: float,
                    estoque: int,
                    estoque_minimo: Optional[int] = None,
                    estoque_alerta: Optional[int] = None,
                    estoque_maximo: Optional[int] = None,
                    preco_aquisicao: Optional[float] = None,
                    categoria: Optional[str] = None,
                    local: Optional[str] = None) -> Material:
    db = get_db_auth()
    try:
        db_material = Material(nome=nome,
                               preco_atual=preco_atual,
                               estoque=estoque,
                               estoque_minimo=estoque_minimo,
                               estoque_alerta=estoque_alerta,
                               estoque_maximo=estoque_maximo,
                               preco_aquisicao=preco_aquisicao,
                               categoria=categoria,
                               local=local)
        db.add(db_material)
        db.commit()
        db.refresh(db_material)
        return db_material
    except IntegrityError:
        db.rollback()
        raise ValueError("Erro ao criar material. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao criar material: {str(e)}")
    finally:
        db.close()

def get_material(material_id: int) -> Optional[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).filter(Material.id == material_id).first()
    finally:
        db.close()

def get_material_by_nome(nome: str) -> Optional[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).filter(Material.nome == nome).first()
    finally:
        db.close()

def get_materiais(skip: int = 0, limit: int = 100) -> List[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).offset(skip).limit(limit).all()
    finally:
        db.close()

def get_materiais_abaixo_minimo() -> List[Material]:
    db = get_db_auth()
    try:
        return db.query(Material).filter(Material.estoque < Material.estoque_minimo).all()
    finally:
        db.close()

def update_material(material_id: int,
                    nome: Optional[str] = None,
                    preco_atual: Optional[float] = None, 
                    estoque: Optional[int] = None,
                    estoque_minimo: Optional[int] = None,
                    estoque_alerta: Optional[int] = None,
                    estoque_maximo: Optional[int] = None,
                    preco_aquisicao: Optional[float] = None, 
                    categoria: Optional[str] = None,
                    local: Optional[str] = None) -> Optional[Material]:
    db = get_db_auth()
    try:
        db_material = db.query(Material).filter(Material.id == material_id).first()
        if db_material:
            if nome:
                db_material.nome = nome
            if preco_atual is not None:
                db_material.preco_atual = preco_atual
            if estoque is not None:
                db_material.estoque = estoque
            if preco_aquisicao is not None:
                db_material.preco_aquisicao = preco_aquisicao
            if categoria:
                db_material.categoria = categoria
            if estoque_minimo is not None:
                db_material.estoque_minimo = estoque_minimo
            if estoque_alerta is not None:
                db_material.estoque_alerta = estoque_alerta
            if estoque_maximo is not None:
                db_material.estoque_maximo = estoque_maximo
            if local:
                db_material.local = local
            db.commit()
            db.refresh(db_material)
        return db_material
    except IntegrityError:
        db.rollback()
        raise ValueError("Erro ao atualizar material. Verifique se todos os campos estão preenchidos corretamente.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao atualizar material: {str(e)}")
    finally:
        db.close()

def delete_material(material_id: int) -> bool:
    db = get_db_auth()
    try:
        db_material = db.query(Material).filter(Material.id == material_id).first()
        if db_material:
            db.delete(db_material)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao deletar material: {str(e)}")
    finally:
        db.close()

#============================================================================
# Funções para gerenciar base de materiais
#============================================================================

def adicionar_materiais(produto_id, material_id) -> MaterialProduto:
    db = get_db_auth()
    try:
        db_produto = db.query(Produto).filter(Produto.id == produto_id).first
        db_material = db.query(Material).filter(Material.id == material_id).first()
        
        if not db_produto or not db_material:
            raise ValueError("Produto ou Material não encontrado.")
        
        material_produto = MaterialProduto(
            produto_id=produto_id,
            material_id=material_id,
        )
        db.add(material_produto)
        db.commit()
        db.refresh(material_produto)
        return material_produto
    except:
        db.rollback()
        raise ValueError("Erro ao adicionar material ao produto.")
    finally:
        db.close()

def remover_materiais(produto_id, material_id):
    db = get_db_auth()
    try:
        material_produto = db.query(MaterialProduto).filter(
            MaterialProduto.produto_id == produto_id,
            MaterialProduto.material_id == material_id
        ).first()
        if material_produto:
            db.delete(material_produto)
            db.commit()
            return True
        return False
    except:
        db.rollback()
        raise ValueError("Erro ao remover material do produto.")
    finally:
        db.close()

def get_materiais_do_produto(produto_id: int) -> List[MaterialProduto]:
    db = get_db_auth()
    try:
        return db.query(MaterialProduto).join(Material).filter(
            MaterialProduto.produto_id == produto_id
        ).all()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao buscar materiais do produto: {str(e)}")
    finally:
        db.close()

def get_produtos_com_material(produto_id: int) -> List[MaterialProduto]:
    db = get_db_auth()
    try:
        return db.query(MaterialProduto).join(Produto).filter(
            MaterialProduto.produto_id == produto_id
        ).all()
    finally:
        db.close()
        
def get_materiais_do_produto_abaixo_estoque(produto_id: int) -> List[MaterialProduto]:
    db = get_db_auth()
    try:
        return db.query(MaterialProduto).join(Material).filter(
            and_(
                MaterialProduto.produto_id == produto_id,
                Material.estoque <= Material.estoque_alerta
            )
        ).all()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao buscar materiais do produto abaixo do estoque: {str(e)}")
    finally:
        db.close()
        
    
