import streamlit as st
from db import SessionLocal, get_cliente, get_carrinho_by_cliente, get_itens_by_carrinho, create_venda, add_item_venda, get_vendedor, get_user, remove_item_from_carrinho
from tools.auth import not_authenticated, get_current_user

def finalizar_compra_page(cliente_id):
    st.title("Finalizar Compra")
    
    db.close()