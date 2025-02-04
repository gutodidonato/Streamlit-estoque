import streamlit as st
from db import SessionLocal, get_cliente, get_carrinho_by_cliente, get_itens_by_carrinho, add_item_to_carrinho, remove_item_from_carrinho, get_produtos
from tools.auth import not_authenticated

def carrinho_page():
    st.title("Gerenciamento de Carrinhos")

    if 'carrinhos_ativos' not in st.session_state or not st.session_state.carrinhos_ativos:
        st.info("Nenhum carrinho ativo. Inicie um carrinho na página de clientes.")
        if st.button("Voltar para Clientes"):
            st.session_state.page = "clientes"
            st.rerun()
        return

    db = SessionLocal()
    cliente_names = [get_cliente(db, client_id).nome for client_id in st.session_state.carrinhos_ativos]
    tabs = st.tabs(cliente_names)

    for i, cliente_id in enumerate(st.session_state.carrinhos_ativos):
        with tabs[i]:
            exibir_carrinho(db, cliente_id)

    db.close()

    if st.sidebar.button("Voltar para Clientes"):
        st.session_state.page = "clientes"
        st.rerun()

def exibir_carrinho(db, cliente_id):
    cliente = get_cliente(db, cliente_id)
    carrinho = get_carrinho_by_cliente(db, cliente_id)
    
    st.header(f"Carrinho de {cliente.nome}")
    
    if carrinho:
        itens = get_itens_by_carrinho(db, carrinho.id)
        if itens:
            total = 0
            for item in itens:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"{item.produto.nome}")
                with col2:
                    st.write(f"Quantidade: {item.quantidade}")
                with col3:
                    subtotal = item.produto.preco_atual * item.quantidade
                    st.write(f"R$ {subtotal:.2f}")
                    total += subtotal
                with col4:
                    if st.button("Remover", key=f"remove_{cliente.id}_{item.id}"):
                        if remove_item_from_carrinho(db, cliente.id, item.produto_id):
                            st.success(f"{item.produto.nome} removido do carrinho!")
                            st.rerun()
                        else:
                            st.error("Erro ao remover item do carrinho.")
            
            st.write(f"**Total: R$ {total:.2f}**")
            
            if st.button("Finalizar Compra", key=f"finish_{carrinho.id}"):
                # JAJA será corrigido
                
                
                
                
                st.success("Compra finalizada com sucesso!")
                st.session_state.carrinhos_ativos.remove(cliente_id)
                st.rerun()
        else:
            st.info("O carrinho está vazio.")
        
    else:
        st.error("Carrinho não encontrado.")

if not_authenticated():
    st.stop()
else:
    carrinho_page()