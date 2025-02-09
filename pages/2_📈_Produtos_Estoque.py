import streamlit as st
import pandas as pd
import numpy as np
from db import SessionLocal, get_produtos, create_produto, update_produto, delete_produto, add_item_to_carrinho, get_cliente
from tools.auth import not_authenticated
from utils import load_product_data, pesquisa_produtos, listagem_produtos, adiciona_produtos

def produto_page():
    st.title("Gerenciamento de Produtos")
    
    df = load_product_data()
    
    aba1, aba2, aba3 = st.tabs(['Listagem Produtos', 'Pesquisa Produtos', 'Adicionar Produto'])

    with aba1:
        listagem_produtos(df)
            
    with aba2:
        pesquisa_produtos(df)

    with aba3:
        adiciona_produtos()
        
if not_authenticated():
    st.stop()
else:
    produto_page()