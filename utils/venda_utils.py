import streamlit as st
import pandas as pd
import numpy as np
from db import SessionLocal, get_produtos, create_produto, update_produto, delete_produto, add_item_to_carrinho, get_cliente, update_item_carrinho, get_materiais_do_produto
from tools.auth import not_authenticated
import time


def progress_bar(estoque: int, estoque_maximo: int, estoque_alerta: int):
    if estoque_maximo == 0 or estoque_alerta == 0:
        st.error("Erro: Estoque máximo ou estoque de alerta não podem ser zero.")
        return
    
    if estoque > estoque_maximo:
        progress = min(100, int((estoque / estoque_maximo) * 100))
        st.progress(progress)
        st.warning("Estamos acima do Estoque Máximo!")
    elif estoque > estoque_alerta:
        progress = min(100, int((estoque / estoque_maximo) * 100))
        st.progress(progress)
        st.success("Estoque em níveis adequados.")
    else:
        progress = min(100, int((estoque / estoque_alerta) * 100))
        st.progress(progress)
        st.error("Estoque crítico! Necessário reabastecer imediatamente.")
    

def load_product_data():
    produtos = get_produtos()
    return pd.DataFrame([
        {
            'id': p.id,
            'nome': p.nome,
            'preco_atual': p.preco_atual,
            'estoque': p.estoque,
            'estoque_minimo': p.estoque_minimo,
            'estoque_alerta': p.estoque_alerta,
            'estoque_maximo': p.estoque_maximo,          
            'preco_aquisicao': p.preco_aquisicao,
            'categoria': p.categoria,
            'local': p.local
        } for p in produtos
    ])
    
def produto(row, informacoes: bool = False, variavel_alerta : int = 0):
    with st.expander(f"{row['nome']} - R$ {row['preco_atual']:.2f}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Categoria: {row['categoria']}")
            st.write(f"Estoque: {row['estoque']}")
            
            if informacoes:
                st.write(f"Estoque Mínimo: {row['estoque_minimo']}")
                st.write(f"Estoque Alerta: {row['estoque_alerta']}")
                st.write(f"Estoque Máximo: {row['estoque_maximo']}")
                st.write(f"Preço de Aquisição: R$ {row['preco_aquisicao']:.2f}")
                if row['preco_atual'] > 0:
                    margem_lucro = ((row['preco_atual'] - row['preco_aquisicao']) / row['preco_atual']) * 100
                    st.write(f"Margem de Lucro: {margem_lucro:.2f}%")
                
            st.write(f"Local: {row['local']}")

            progress = progress_bar(estoque=row['estoque'], estoque_alerta=row['estoque_alerta'], estoque_maximo=row['estoque_maximo'])
        with col2:
            if row['estoque'] > 0:
                quantidade = st.number_input(f"Quantidade", min_value=1, max_value=row['estoque'], value=1, key=f"qty_{row['id']}_{variavel_alerta}")
                carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])
                if carrinhos_ativos:
                    carrinho_id = st.selectbox("Selecione o carrinho", options=carrinhos_ativos, format_func=lambda x: get_cliente(x).nome, key=f"carrinho_{row['id']}_{variavel_alerta}")
                    if st.button("Adicionar ao Carrinho", key=f"add_{row['id']}_{variavel_alerta}"):
                        if add_item_to_carrinho(carrinho_id, row['id'], quantidade):
                            st.success(f"{quantidade} {row['nome']} adicionado(s) ao carrinho!")
                        else:
                            st.error("Erro ao adicionar ao carrinho.")
                else:
                    st.warning("Nenhum carrinho ativo.")
            else:
                st.warning("Produto fora de estoque")
                    
            

                        
def listagem_produtos(df):
    st.header("Listagem Simples de Produtos", divider='blue')
    try:
        categorias = df['categoria'].unique().tolist()
        tabs = st.tabs(categorias)
        carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])

        for i, categoria in enumerate(categorias):
            with tabs[i]:
                produtos_categoria = df[df['categoria'] == categoria]
                for index, row in produtos_categoria.iterrows():
                    produto(row, informacoes=False, variavel_alerta=1)
    except Exception as e:
        st.warning(f'Crie os produtos !')
        print(e)

def pesquisa_produtos(df):
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
            for index, row in produtos_filtrados.iterrows():
                produto(row, False, 2)
                
                
def pesquisa_produtos_avançado(df):
    st.header("Pesquisa Avançada de Produtos")
    search_term_1 = st.text_input("Digite o nome do produto, categoria ou qualquer outra informação", key="busca_avancada")
    if search_term_1:
        produtos_filtrados = df[
            df.astype(str).apply(lambda x: x.str.contains(search_term_1, case=False)).any(axis=1)
        ]
                    
        if produtos_filtrados.empty:
            st.warning("Nenhum produto encontrado com esse termo de pesquisa.")
        else:
            st.success(f"{len(produtos_filtrados)} produto(s) encontrado(s).")
            for index, row in produtos_filtrados.iterrows():
                produto(row, True, 6)    



def adiciona_produtos():
    st.header("Adicionar Produtos", divider='red')
    with st.form("novo_produto"):
        nome = st.text_input("Nome do Produto")
        preco_atual = st.number_input("Preço de Venda", min_value=0.01, step=0.01)
        estoque = st.number_input("Estoque", min_value=0, step=1)
        estoque_minimo = st.number_input("Estoque Mínimo", min_value=0, step=1)
        estoque_alerta = st.number_input("Estoque Alerta", min_value=0, step=1)
        estoque_maximo = st.number_input("Estoque Máximo", min_value=0, step=1)
        preco_aquisicao = st.number_input("Preço de Aquisição", min_value=0.0, step=0.01)
        categoria = st.text_input("Categoria")
        local = st.text_input("Local")
        if st.form_submit_button("Adicionar Produto"):
            novo_produto = create_produto(nome, preco_atual, estoque, estoque_minimo, estoque_alerta, estoque_maximo, preco_aquisicao, categoria, local)
            if novo_produto:
                st.success(f"Produto '{nome}' adicionado com sucesso!")
                time.sleep(3)
                st.rerun()
            else:
                st.error("Erro ao adicionar produto.")
                time.sleep(3)
                st.rerun()
                
def listagem_produtos_detalhada(df):
    try:
        st.header("Listagem Avançada de Produtos", divider='blue')
        categorias = df['categoria'].unique().tolist()
        tabs = st.tabs(categorias)
        carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])

        for i, categoria in enumerate(categorias):
            with tabs[i]:
                produtos_categoria = df[df['categoria'] == categoria]
                for index, row in produtos_categoria.iterrows():
                    produto(row, True, 4)
    except Exception as e:
        st.warning(f'Crie os produtos !')
        print(e)
        
        
def pesquisa_e_edicao_produtos(df, variavel_alerta : int = 9):
    st.header("Edição de Produtos", divider='red')

    # Campo de pesquisa
    search_term = st.text_input("Digite o nome do produto, categoria ou qualquer outra informação", key=f"{variavel_alerta}_123")

    if search_term:
        produtos_filtrados = df[
            df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        ]

        if produtos_filtrados.empty:
            st.warning("Nenhum produto encontrado com esse termo de pesquisa.")
        else:
            st.success(f"{len(produtos_filtrados)} produto(s) encontrado(s).")
            for index, row in produtos_filtrados.iterrows():
                with st.expander(f"{row['nome']} - R$ {row['preco_atual']:.2f}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"Categoria: {row['categoria']}")
                        st.write(f"Local: {row['local']}")
                        st.write(f"Categoria: {row['categoria']}")
                        st.write(f"Estoque: {row['estoque']}")
                        st.write(f"Estoque Mínimo: {row['estoque_minimo']}")
                        st.write(f"Estoque Alerta: {row['estoque_alerta']}")
                        st.write(f"Estoque Máximo: {row['estoque_maximo']}")
                        st.write(f"Preço de Aquisição: R$ {row['preco_aquisicao']:.2f}")
                        

                    with col2:
                        if st.button("Deletar", key=f"del_{row['id']}_{variavel_alerta}"):
                            if st.button("Confirmar exclusão?", key=f"confirm_del_{row['id']}_{variavel_alerta}"):
                                if delete_produto(row['id']):
                                    st.success(f"Produto '{row['nome']}' deletado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao deletar produto.")
                                    
                                    
                        if st.button("Editar", key=f"edit_{index}"):
                            st.session_state[f"editing_{index}"] = True

                    if st.session_state.get(f"editing_{index}", False):
                        with st.form(key=f"edit_form_{index}"):
                            key_prefix = f"editing_{index}_{variavel_alerta}"
                            nome_edit = st.text_input("Nome do Produto", value=row['nome'], key=f"{key_prefix}_nome")
                            preco_atual_edit = st.number_input("Preço de Venda", min_value=0.01, step=0.01, value=float(row['preco_atual']), key=f"{key_prefix}_preco_atual")
                            estoque_edit = st.number_input("Estoque", min_value=0, step=1, value=int(row['estoque']), key=f"{key_prefix}_estoque")
                            estoque_minimo_edit = st.number_input("Estoque Mínimo", min_value=0, step=1, value=int(row['estoque_minimo']), key=f"{key_prefix}_estoque_minimo")
                            estoque_alerta_edit = st.number_input("Estoque Alerta", min_value=0, step=1, value=int(row['estoque_alerta']), key=f"{key_prefix}_estoque_alerta")
                            estoque_maximo_edit = st.number_input("Estoque Máximo", min_value=0, step=1, value=int(row['estoque_maximo']), key=f"{key_prefix}_estoque_maximo")
                            preco_aquisicao_edit = st.number_input("Preço de Aquisição", min_value=0.0, step=0.01, value=float(row['preco_aquisicao']), key=f"{key_prefix}_preco_aquisicao")
                            categoria_edit = st.text_input("Categoria", value=row['categoria'], key=f"{key_prefix}_categoria")
                            local_edit = st.text_input("Local", value=row['local'], key=f"{key_prefix}_local")

                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    update_produto(
                                        produto_id=row['id'],
                                        nome=nome_edit,
                                        preco_atual=preco_atual_edit,
                                        estoque=estoque_edit,
                                        estoque_minimo=estoque_minimo_edit,
                                        estoque_alerta=estoque_alerta_edit,
                                        estoque_maximo=estoque_maximo_edit,
                                        preco_aquisicao=preco_aquisicao_edit,
                                        categoria=categoria_edit,
                                        local=local_edit
                                    )
                                    st.success("Produto atualizado com sucesso!")
                                    st.session_state[f"editing_{index}"] = False
                                    st.rerun()
                            with col2:
                                if st.form_submit_button("Cancelar"):
                                    st.session_state[f"editing_{index}"] = False
                                    st.rerun()