import streamlit as st
from tools.auth import not_authenticated
from db.main import init_db

def main():
    produtos = st.Page(
        page='pages/2_📈_Produtos_Estoque.py',
        default=True,
        title='Produtos e Estoque'
    )
    clientes = st.Page(
        page='pages/3_👦_Clientes.py',
        title='Página de Clientes'
    )
    carrinhos = st.Page(
        page='pages/4_🛒_Carrinhos.py',
        title='Carrinhos Ativos'
    )
    vendas = st.Page(
        page='pages/5_💸_Vendas.py',
        title='Vendas'
    )
    estoques = st.Page(
        page='pages/6_🧳_Materiais_Estoque.py',
        title='Materiais'
    )
    configuracoes = st.Page(
        page='pages/10_⚙️_Configurações.py',
        title='Configurações',
    )
    pg = st.navigation(
        {
            "Vendas": [produtos, clientes, carrinhos, vendas],
            "Materiais": [estoques],
            "Configurações": [configuracoes],
        }
    )
    pg.run()

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado.")
    main()
    
    
    