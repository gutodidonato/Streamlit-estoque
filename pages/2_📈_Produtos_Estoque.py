import streamlit as st
from tools.auth import not_authenticated
from utils import load_product_data, pesquisa_produtos, listagem_produtos, adiciona_produtos, listagem_produtos_detalhada, pesquisa_e_edicao_produtos

def produto_page():
    st.title("Gerenciamento de Produtos")
    
    df = load_product_data()
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs(['Listagem Produtos', 'Pesquisa Produtos', 'Adicionar Produto', 'Listagem Avançada', 'Edição de Produtos'])

    with aba1:
        listagem_produtos(df)
            
    with aba2:
        pesquisa_produtos(df)

    with aba3:
        adiciona_produtos()
        
    with aba4:
        listagem_produtos_detalhada(df)
    with aba5:
        pesquisa_e_edicao_produtos(df)
        
        
if not_authenticated():
    st.stop()
else:
    produto_page()