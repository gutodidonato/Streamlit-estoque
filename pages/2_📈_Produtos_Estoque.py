import streamlit as st
import pandas as pd
import numpy as np
from db import SessionLocal, get_produtos, create_produto, update_produto, delete_produto, add_item_to_carrinho, get_cliente
from tools.auth import not_authenticated

def load_product_data():
    db = SessionLocal()
    produtos = get_produtos(db)
    db.close()
    return pd.DataFrame([
        {
            'id': p.id,
            'nome': p.nome,
            'preco_atual': p.preco_atual,
            'estoque': p.estoque,
            'preco_aquisicao': p.preco_aquisicao,
            'categoria': p.categoria
        } for p in produtos
    ])

def produto_page():
    st.title("Gerenciamento de Produtos")
    
    # Carregar dados
    df = load_product_data()
    
    aba1, aba2, aba3 = st.tabs(['Listagem Produtos', 'Pesquisa Produtos', 'Adicionar Produto'])

    with aba1:
        categorias = df['categoria'].unique().tolist()
        
        if not categorias:
            st.warning("Não há produtos cadastrados.")
        else:
            tabs = st.tabs(categorias)
            carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])
            
            print(categorias)

            for i, categoria in enumerate(categorias):
                with tabs[i]:
                    produtos_categoria = df[df['categoria'] == categoria]
                    for _, row in produtos_categoria.iterrows():
                        with st.expander(f"{row['nome']} - R$ {row['preco_atual']:.2f}"):
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.write(f"Estoque: {row['estoque']}")
                                st.write(f"Preço de Aquisição: R$ {row['preco_aquisicao']:.2f}")
                                if row['preco_atual'] > 0:
                                    margem_lucro = ((row['preco_atual'] - row['preco_aquisicao']) / row['preco_atual']) * 100
                                    st.write(f"Margem de Lucro: {margem_lucro:.2f}%")
                            
                            with col2:
                                if row['estoque'] > 0:
                                    quantidade = st.number_input(f"Quantidade para {row['nome']}", min_value=1, max_value=row['estoque'], value=1, key=f"qty_{row['id']}")
                                else:
                                    st.write("Produto fora de estoque")
                                    quantidade = 0
                            
                            with col3:
                                if carrinhos_ativos and row['estoque'] > 0:
                                    for carrinho_id in carrinhos_ativos:
                                        db = SessionLocal()
                                        cliente = get_cliente(db, carrinho_id)
                                        db.close()
                                        if st.button(f"Adicionar ao Carrinho de {cliente.nome}", key=f"add_{row['id']}_{carrinho_id}"):
                                            db = SessionLocal()
                                            if add_item_to_carrinho(db, carrinho_id, row['id'], quantidade):
                                                st.success(f"{quantidade} {row['nome']} adicionado(s) ao Carrinho de {cliente.nome}!")
                                            else:
                                                st.error("Erro ao adicionar ao carrinho.")
                                            db.close()
                                elif row['estoque'] == 0:
                                    st.warning("Produto fora de estoque")
                                else:
                                    st.warning("Nenhum carrinho ativo. Inicie um carrinho na página de clientes.")
                            
                            if st.button(f"Deletar {row['nome']}", key=f"del_{row['id']}"):
                                db = SessionLocal()
                                if delete_produto(db, row['id']):
                                    st.success(f"Produto '{row['nome']}' deletado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao deletar produto.")
                                db.close()
                            
                            if st.button(f"Atualizar {row['nome']}", key=f"upd_{row['id']}"):
                                st.session_state.editing_product = row['id']
                            
                            if st.session_state.get('editing_product') == row['id']:
                                st.header(f"Editar Produto : {row['nome']}")
                                with st.form(f"editar_produto_{row['id']}"):
                                    nome = st.text_input("Nome do Produto", value=row['nome'])
                                    preco_atual = st.number_input("Preço de Venda", min_value=0.01, step=0.01, value=float(row['preco_atual']))
                                    estoque = st.number_input("Estoque", min_value=0, step=1, value=int(row['estoque']))
                                    preco_aquisicao = st.number_input("Preço de Aquisição", min_value=0.0, step=0.01, value=float(row['preco_aquisicao']))
                                    categoria = st.text_input("Categoria", value=row['categoria'])
                                    if st.form_submit_button("Atualizar produto"):
                                        db = SessionLocal()
                                        if update_produto(db, row['id'], nome, preco_atual, estoque, preco_aquisicao, categoria):
                                            st.success("Produto atualizado com sucesso!")
                                            del st.session_state.editing_product
                                            st.rerun()
                                        else:
                                            st.error("Erro ao atualizar produto.")
                                        db.close()
        with aba2:
            st.header("Pesquisar Produtos")
            search_term = st.text_input("Digite o nome do produto, categoria ou qualquer outra informação")
            
            if search_term:
                produtos_filtrados = df[
                    df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
                ]
                
                if produtos_filtrados.empty:
                    st.warning("Nenhum produto encontrado com esse termo de pesquisa.")
                else:
                    st.success(f"{len(produtos_filtrados)} produto(s) encontrado(s).")
                    for _, row in produtos_filtrados.iterrows():
                        with st.expander(f"{row['nome']} - R$ {row['preco_atual']:.2f}"):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"Categoria: {row['categoria']}")
                                st.write(f"Estoque: {row['estoque']}")
                                st.write(f"Preço de Aquisição: R$ {row['preco_aquisicao']:.2f}")
                                if row['preco_atual'] > 0:
                                    margem_lucro = ((row['preco_atual'] - row['preco_aquisicao']) / row['preco_atual']) * 100
                                    st.write(f"Margem de Lucro: {margem_lucro:.2f}%")
                            
                            with col2:
                                if row['estoque'] > 0:
                                    quantidade = st.number_input(f"Quantidade", min_value=1, max_value=row['estoque'], value=1, key=f"qty_search_{row['id']}")
                                    carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])
                                    if carrinhos_ativos:
                                        carrinho_id = st.selectbox("Selecione o carrinho", options=carrinhos_ativos, format_func=lambda x: get_cliente(SessionLocal(), x).nome, key=f"carrinho_select_{row['id']}")
                                        if st.button("Adicionar ao Carrinho", key=f"add_search_{row['id']}"):
                                            db = SessionLocal()
                                            if add_item_to_carrinho(db, carrinho_id, row['id'], quantidade):
                                                st.success(f"{quantidade} {row['nome']} adicionado(s) ao carrinho!")
                                            else:
                                                st.error("Erro ao adicionar ao carrinho.")
                                            db.close()
                                    else:
                                        st.warning("Nenhum carrinho ativo.")
                                else:
                                    st.warning("Produto fora de estoque")
                            
                            col3, col4 = st.columns(2)
                            with col3:
                                if st.button(f"Deletar", key=f"del_search_{row['id']}"):
                                    db = SessionLocal()
                                    if delete_produto(db, row['id']):
                                        st.success(f"Produto '{row['nome']}' deletado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error("Erro ao deletar produto.")
                                    db.close()
                            with col4:
                                if st.button(f"Atualizar", key=f"upd_search_{row['id']}"):
                                    st.session_state.editing_product = row['id']
                            
                            if st.session_state.get('editing_product') == row['id']:
                                st.header(f"Editar Produto : {row['nome']}")
                                with st.form(f"editar_produto_search_{row['id']}"):
                                    nome = st.text_input("Nome do Produto", value=row['nome'])
                                    preco_atual = st.number_input("Preço de Venda", min_value=0.01, step=0.01, value=float(row['preco_atual']))
                                    estoque = st.number_input("Estoque", min_value=0, step=1, value=int(row['estoque']))
                                    preco_aquisicao = st.number_input("Preço de Aquisição", min_value=0.0, step=0.01, value=float(row['preco_aquisicao']))
                                    categoria = st.text_input("Categoria", value=row['categoria'])
                                    if st.form_submit_button("Atualizar produto"):
                                        db = SessionLocal()
                                        if update_produto(db, row['id'], nome, preco_atual, estoque, preco_aquisicao, categoria):
                                            st.success("Produto atualizado com sucesso!")
                                            del st.session_state.editing_product
                                            st.rerun()
                                        else:
                                            st.error("Erro ao atualizar produto.")
                                        db.close()

    with aba3:
        with st.form("novo_produto"):
            nome = st.text_input("Nome do Produto")
            preco_atual = st.number_input("Preço de Venda", min_value=0.01, step=0.01)
            estoque = st.number_input("Estoque", min_value=0, step=1)
            preco_aquisicao = st.number_input("Preço de Aquisição", min_value=0.0, step=0.01)
            categoria = st.text_input("Categoria")

            if st.form_submit_button("Adicionar Produto"):
                db = SessionLocal()
                novo_produto = create_produto(db, nome, preco_atual, estoque, preco_aquisicao, categoria)
                if novo_produto:
                    st.success(f"Produto '{nome}' adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar produto.")
                db.close()
                st.rerun()
        
if not_authenticated():
    st.stop()
else:
    produto_page()