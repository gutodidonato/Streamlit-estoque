import streamlit as st
import pandas as pd
import numpy as np
from db import SessionLocal, get_produtos, create_produto, update_produto, delete_produto, add_item_to_carrinho, get_cliente, update_item_carrinho, get_materiais_do_produto
from tools.auth import not_authenticated
import time

produto_counter = 0

def progress_bar(estoque, estoque_alerta):
    if estoque_alerta == 0:
        return 100 
    progress = min(100, (estoque / estoque_alerta) * 100)
    return progress

def load_product_data():
    global produto_counter
    produto_counter += 1
    
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
    
def produto(row, index, informacoes: bool = False):
    global produto_counter
    produto_counter += 1
    

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

            progress = progress_bar(row['estoque'], row['estoque_alerta'])
            st.write("Status do Estoque:")
            col_bar, col_text = st.columns([3, 1])
            with col_bar:
                st.progress(progress / 100)
            with col_text:
                st.write(f"{progress:.1f}%")
            
            if progress < 20:
                st.error("Estoque crítico! Necessário reabastecer imediatamente.")
            elif progress < 50:
                st.warning("Estoque baixo! Considere reabastecer em breve.")
            else:
                st.success("Estoque em níveis adequados.")
                    
        with col2:
            if row['estoque'] > 0:
                quantidade = st.number_input(f"Quantidade", min_value=1, max_value=row['estoque'], value=1, key=f"qty_{row['id']}_{produto_counter}")
                carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])
                if carrinhos_ativos:
                    carrinho_id = st.selectbox("Selecione o carrinho", options=carrinhos_ativos, format_func=lambda x: get_cliente(x).nome, key=f"carrinho_{row['id']}_{produto_counter}")
                    if st.button("Adicionar ao Carrinho", key=f"add_{row['id']}_{produto_counter}"):
                        if add_item_to_carrinho(carrinho_id, row['id'], quantidade):
                            st.success(f"{quantidade} {row['nome']} adicionado(s) ao carrinho!")
                        else:
                            st.error("Erro ao adicionar ao carrinho.")
                else:
                    st.warning("Nenhum carrinho ativo.")
            else:
                st.warning("Produto fora de estoque")
                    
            if st.button("Deletar", key=f"del_{row['id']}_{produto_counter}"):
                if st.button("Confirmar exclusão?", key=f"confirm_del_{row['id']}_{produto_counter}"):
                    if delete_produto(row['id']):
                        st.success(f"Produto '{row['nome']}' deletado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao deletar produto.")
            

                        
def listagem_produtos(df):
    try:
        categorias = df['categoria'].unique().tolist()
        tabs = st.tabs(categorias)
        carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])

        for i, categoria in enumerate(categorias):
            with tabs[i]:
                produtos_categoria = df[df['categoria'] == categoria]
                for index, row in produtos_categoria.iterrows():
                    produto(row, index)
    except Exception as e:
        st.error(f'Erro ao listar produtos: {str(e)}')

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
                produto(row, index)

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
            for _, row in produtos_filtrados.iterrows():
                produto(row)

def adiciona_produtos():
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
        categorias = df['categoria'].unique().tolist()
        tabs = st.tabs(categorias)
        carrinhos_ativos = st.session_state.get('carrinhos_ativos', [])

        for i, categoria in enumerate(categorias):
            with tabs[i]:
                produtos_categoria = df[df['categoria'] == categoria]
                for index, row in produtos_categoria.iterrows():
                    produto(row, index, True)
    except Exception as e:
        st.error(f'Erro ao listar produtos: {str(e)}')
        
        
def pesquisa_e_edicao_produtos(df):
    st.header("Edição de Produtos")

    # Campo de pesquisa
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
                with st.expander(f"{row['nome']} - R$ {row['preco_atual']:.2f}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"Categoria: {row['categoria']}")
                        st.write(f"Estoque: {row['estoque']}")
                        st.write(f"Local: {row['local']}")
                        
                        # Barra de progresso para o estoque
                        progress = min(100, (row['estoque'] / row['estoque_maximo']) * 100) if row['estoque_maximo'] > 0 else 0
                        st.progress(progress)
                        if progress < 20:
                            st.error("Estoque crítico!")
                        elif progress < 50:
                            st.warning("Estoque baixo!")
                        else:
                            st.success("Estoque adequado")

                    with col2:
                        if st.button("Editar", key=f"edit_{index}"):
                            st.session_state[f"editing_{index}"] = True

                    if st.session_state.get(f"editing_{index}", False):
                        with st.form(key=f"edit_form_{index}"):
                            nome = st.text_input("Nome do Produto", value=row['nome'])
                            preco_atual = st.number_input("Preço de Venda", min_value=0.01, step=0.01, value=float(row['preco_atual']))
                            estoque = st.number_input("Estoque", min_value=0, step=1, value=int(row['estoque']))
                            estoque_minimo = st.number_input("Estoque Mínimo", min_value=0, step=1, value=int(row['estoque_minimo']))
                            estoque_alerta = st.number_input("Estoque Alerta", min_value=0, step=1, value=int(row['estoque_alerta']))
                            estoque_maximo = st.number_input("Estoque Máximo", min_value=0, step=1, value=int(row['estoque_maximo']))
                            preco_aquisicao = st.number_input("Preço de Aquisição", min_value=0.0, step=0.01, value=float(row['preco_aquisicao']))
                            categoria = st.text_input("Categoria", value=row['categoria'])
                            local = st.text_input("Local", value=row['local'])

                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    update_produto(
                                        nome=nome,
                                        preco_atual=preco_atual,
                                        estoque=estoque,
                                        estoque_minimo=estoque_minimo,
                                        estoque_alerta=estoque_alerta,
                                        estoque_maximo=estoque_maximo,
                                        preco_aquisicao=preco_aquisicao,
                                        categoria=categoria,
                                        local=local
                                    )
                                    st.success("Produto atualizado com sucesso!")
                                    st.session_state[f"editing_{index}"] = False
                                    st.rerun()
                            with col2:
                                if st.form_submit_button("Cancelar"):
                                    st.session_state[f"editing_{index}"] = False
                                    st.rerun()