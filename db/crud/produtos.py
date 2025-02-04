from ..models import Produto

def create_produto(db, nome, preco_atual, estoque=0, preco_aquisicao=0, categoria=None) -> object | None:
    produto = Produto(
        nome=nome,
        preco_atual=preco_atual,
        estoque=estoque,
        preco_aquisicao=preco_aquisicao,
        categoria=categoria
        
    )
    try:
        db.add(produto)
        db.commit()
        db.refresh(produto)
        return produto
    except Exception as e:
        db.rollback()
        raise e
    
def get_produto(db, id_produto: int) -> object | None:
    return db.query(Produto).filter(Produto.id == id_produto).first()

def get_produto_by_nome(db, nome: str) -> object | None:
    return db.query(Produto).filter(Produto.nome == nome).first()

def update_produto(db, id_produto, nome, preco_atual, estoque=0, preco_aquisicao=0, categoria=None):
    produto = get_produto(db, id_produto)
    if produto:
          db.update() 