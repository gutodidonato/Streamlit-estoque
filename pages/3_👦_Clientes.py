import streamlit as st
from db import SessionLocal, create_cliente, select_cliente_all, update_cliente, delete_cliente
from tools.auth import not_authenticated




def cliente_page():
    st.title("Gerenciamento de Clientes")

    # Formulário para adicionar novo cliente
    aba1, aba2 = st.tabs(['Adicionar Clientes', 'Listagem'])
    with aba1:
        with st.form("novo_cliente"):
            nome = st.text_input("Nome")
            endereco = st.text_input("Endereço")
            telefone = st.text_input("Telefone")
            email = st.text_input("Email")
            if st.form_submit_button("Adicionar Cliente"):
                db = SessionLocal()
                try:
                    create_cliente(db, nome, endereco, telefone, email)
                    st.success("Cliente adicionado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
                finally:
                    db.close()

    with aba2:
    # Lista de clientes
        st.subheader("Lista de Clientes")
        db = SessionLocal()
        clientes = select_cliente_all(db)
        for cliente in clientes:
            with st.expander(f"{cliente.nome}"):
                st.write(f"Endereço: {cliente.endereco}")
                st.write(f"Telefone: {cliente.telefone}")
                st.write(f"Email: {cliente.email}")
                if st.button("Deletar", key=f"del_{cliente.id}"):
                    if delete_cliente(db, cliente.id):
                        st.success("Cliente deletado com sucesso!")
                        st.rerun()
        db.close()

if not_authenticated():
    st.stop()
cliente_page()