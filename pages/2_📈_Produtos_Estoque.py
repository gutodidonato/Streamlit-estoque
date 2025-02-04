from tools.auth import not_authenticated
import streamlit as st
import pandas as pd
import plotly.express as px

def load_product_data():
    return pd.DataFrame({
        'nome': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
        'categoria': ['Eletrônicos', 'Roupas', 'Alimentos', 'Eletrônicos', 'Roupas'],
        'preco': [100, 50, 10, 200, 75],
        'estoque': [50, 100, 200, 30, 80],
        'avaliacao': [4.5, 3.8, 4.2, 4.7, 4.0]
    })

def main():
    st.set_page_config(layout="wide", page_title="Catálogo de Produtos")
    
    st.title("Catálogo de Produtos")
    
    aba1, aba2 = st.tabs(['Catalogo', 'Dashboard'])
    with aba1:

        df = load_product_data()

        # Sidebar para filtros
        st.sidebar.header("Filtros")
        categorias = st.sidebar.multiselect("Selecione as categorias", df['categoria'].unique())
        preco_min, preco_max = st.sidebar.slider("Faixa de Preço", float(df['preco'].min()), float(df['preco'].max()), (0.0, float(df['preco'].max())))

        # Aplicar filtros
        if categorias:
            df = df[df['categoria'].isin(categorias)]
        df = df[(df['preco'] >= preco_min) & (df['preco'] <= preco_max)]

        # Agrupar produtos por categoria
        grouped = df.groupby('categoria')

        # Layout principal
        st.subheader("Lista de Produtos")
        for categoria, grupo in grouped:
            with st.expander(f"{categoria} ({len(grupo)} produtos)"):
                for index, row in grupo.iterrows():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.subheader(row['nome'])
                        st.write(f"Preço: R$ {row['preco']:.2f}")
                        st.write(f"Estoque: {row['estoque']} unidades")
                    with col2:
                        st.write(f"Avaliação: {row['avaliacao']:.1f}/5.0")
                        st.progress(row['avaliacao'] / 5)
                    with col3:
                        if st.button(f"Adicionar ao Carrinho", key=f"add_{index}"):
                            st.success(f"{row['nome']} adicionado ao carrinho!")
                    st.markdown("---")

    
    with aba2:
        st.write('Dash')
    
    
    
if not_authenticated():
    st.stop()  
main()

