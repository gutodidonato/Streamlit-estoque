from ..models import Carrinho, Produto, ItemCarrinho, ItemVenda, Venda
from sqlalchemy.orm import Session

def get_or_create_carrinho(session: Session, cliente_id: int):
    carrinho = session.query(Carrinho).filter_by(cliente_id=cliente_id).first()
    if not carrinho:
        carrinho = Carrinho(cliente_id=cliente_id)
        session.add(carrinho)
        session.commit()
    return carrinho

def adicionar_ao_carrinho(session: Session, cliente_id: int, produto_id: int, quantidade: int):
    carrinho = get_or_create_carrinho(session, cliente_id)
    produto = session.query(Produto).get(produto_id)
    
    if produto and produto.estoque >= quantidade:
        item = session.query(ItemCarrinho).filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()
        if item:
            item.quantidade += quantidade
        else:
            item = ItemCarrinho(carrinho_id=carrinho.id, produto_id=produto_id, quantidade=quantidade)
            session.add(item)
        
        session.commit()
        return True
    return False

def remover_do_carrinho(session: Session, cliente_id: int, produto_id: int):
    carrinho = get_or_create_carrinho(session, cliente_id)
    item = session.query(ItemCarrinho).filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()
    if item:
        session.delete(item)
        session.commit()
        return True
    return False

def criar_venda_do_carrinho(session: Session, cliente_id: int, vendedor_id: int, user_id: int, frete: float = 0):
    carrinho = get_or_create_carrinho(session, cliente_id)
    if not carrinho.itens:
        return None
    
    venda = Venda(
        cliente_id=cliente_id,
        vendedor_id=vendedor_id,
        user_id=user_id,
        frete=frete,
        total=frete
    )
    session.add(venda)
    
    for item_carrinho in carrinho.itens:
        produto = item_carrinho.produto
        if produto.estoque < item_carrinho.quantidade:
            session.rollback()
            return None
        
        item_venda = ItemVenda(
            venda=venda,
            produto=produto,
            quantidade=item_carrinho.quantidade,
            preco_unitario=produto.preco
        )
        venda.total += item_venda.quantidade * item_venda.preco_unitario
        produto.estoque -= item_venda.quantidade
    
    session.query(ItemCarrinho).filter_by(carrinho_id=carrinho.id).delete()
    
    session.commit()
    return venda

def finalizar_venda(session: Session, venda_id: int):
    venda = session.query(Venda).get(venda_id)
    if venda and not venda.confirmar:
        venda.confirmar = True
        session.commit()
        return True
    return False

def cancelar_venda(session: Session, venda_id: int):
    venda = session.query(Venda).get(venda_id)
    if venda and not venda.confirmar:
        for item in venda.itens:
            item.produto.estoque += item.quantidade
        session.delete(venda)
        session.commit()
        return True
    return False