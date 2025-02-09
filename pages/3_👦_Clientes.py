import streamlit as st
from db import SessionLocal, create_cliente, get_all_clientes, update_cliente, delete_cliente, get_carrinho_by_cliente, create_carrinho
from tools.auth import not_authenticated


def adicionar_cliente():
    st.header("Adicionar Novo Cliente")
    with st.form("novo_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            endereco = st.text_input("Endereço")
        with col2:
            telefone = st.text_input("Telefone")
            email = st.text_input("Email")
        
        if st.form_submit_button("Adicionar Cliente"):
            st.write(nome, endereco, telefone, email)
            create_cliente(nome=nome, endereco=endereco, telefone=telefone, email=email)
            st.success("Cliente adicionado com sucesso!")

def listagem_clientes():
    st.header("Lista de Clientes")
    clientes = get_all_clientes()
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Buscar cliente por nome ou email")
    with col2:
        sort_option = st.selectbox("Ordenar por:", ["Nome", "Email"])
        reverse = st.checkbox("Ordem decrescente")

    filtered_clientes = [cliente for cliente in clientes if search.lower() in cliente.nome.lower() or (cliente.email and search.lower() in cliente.email.lower())]

    if sort_option == "Nome":
        filtered_clientes.sort(key=lambda x: x.nome.lower(), reverse=reverse)
    else:
        filtered_clientes.sort(key=lambda x: (x.email or "").lower(), reverse=reverse)

    for cliente in filtered_clientes:
        with st.expander(f"Cliente: {cliente.nome} -  Email: {cliente.email or 'Sem email'}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**Email:** {cliente.email or 'Não informado'}")
                st.write(f"**Endereço:** {cliente.endereco or 'Não informado'}")
                st.write(f"**Telefone:** {cliente.telefone or 'Não informado'}")
            with col2:
                if st.button("Iniciar Carrinho", key=f"start_cart_{cliente.id}"):
                    carrinho = get_carrinho_by_cliente(cliente.id)
                    if not carrinho:
                        carrinho = create_carrinho(cliente.id)
                    if 'carrinhos_ativos' not in st.session_state:
                        st.session_state.carrinhos_ativos = []
                        if cliente.id not in st.session_state.carrinhos_ativos:
                            st.session_state.carrinhos_ativos.append(cliente.id)
                            st.success(f"Carrinho iniciado para {cliente.nome}")
            with col3:
                col3_1, col3_2 = st.columns(2)
                with col3_1:
                    if st.button("Editar", key=f"edit_{cliente.id}"):
                        st.session_state.editing_client = cliente.id
                with col3_2:
                    if st.button("Deletar", key=f"del_{cliente.id}"):
                        if delete_cliente(cliente.id):
                            st.success("Cliente deletado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao deletar cliente.")

            if st.session_state.get('editing_client') == cliente.id:
                st.subheader(f"Editar Cliente: {cliente.nome}")
                with st.form(key=f"edit_form_{cliente.id}"):
                    nome = st.text_input("Nome", value=cliente.nome)
                    email = st.text_input("Email", value=cliente.email)
                    endereco = st.text_input("Endereço", value=cliente.endereco)
                    telefone = st.text_input("Telefone", value=cliente.telefone)
                    if st.form_submit_button("Atualizar Cliente"):
                        if update_cliente(cliente.id, nome, endereco, telefone, email):
                            st.success("Cliente atualizado com sucesso!")
                            del st.session_state.editing_client
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar cliente.")
                    

    



def cliente_page():
    st.title("Gerenciamento de Clientes")

    aba1, aba2 = st.tabs(['Adicionar Clientes', 'Listagem de Clientes'])

    with aba1:
        adicionar_cliente()

    with aba2:
        listagem_clientes()

    

if not_authenticated():
    st.stop()
else:
    cliente_page()
