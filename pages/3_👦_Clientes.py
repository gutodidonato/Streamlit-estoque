import streamlit as st
from db import SessionLocal, create_cliente, get_all_clientes, update_cliente, delete_cliente, get_carrinho_by_cliente, create_carrinho
from tools.auth import not_authenticated

def cliente_page():
    st.title("Gerenciamento de Clientes")

    aba1, aba2 = st.tabs(['Adicionar Clientes', 'Listagem de Clientes'])

    with aba1:
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
                db = SessionLocal()
                try:
                    create_cliente(db, nome, endereco, telefone, email)
                    st.success("Cliente adicionado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
                finally:
                    db.close()

    with aba2:
        st.header("Lista de Clientes")
        db = SessionLocal()
        clientes = get_all_clientes(db)
        
        # Adicionar campo de busca
        search = st.text_input("Buscar cliente por nome")
        filtered_clientes = [cliente for cliente in clientes if search.lower() in cliente.nome.lower()]
        
        # Adicionar opções de ordenação
        sort_option = st.selectbox("Ordenar por:", ["Nome", "Email"])
        reverse = st.checkbox("Ordem decrescente")
        
        if sort_option == "Nome":
            filtered_clientes.sort(key=lambda x: x.nome, reverse=reverse)
        else:
            filtered_clientes.sort(key=lambda x: x.email, reverse=reverse)
        
        for cliente in filtered_clientes:
            with st.expander(f"Cliente: {cliente.nome} -  Email: {cliente.email or 'Sem email'}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {cliente.email or 'Não informado'}")
                    st.write(f"**Endereço:** {cliente.endereco or 'Não informado'}")
                    st.write(f"**Telefone:** {cliente.telefone or 'Não informado'}")
                with col2:
                    if st.button("Iniciar Carrinho", key=f"start_cart_{cliente.id}"):
                        carrinho = get_carrinho_by_cliente(db, cliente.id)
                        if not carrinho:
                            carrinho = create_carrinho(db, cliente.id)
                        if 'carrinhos_ativos' not in st.session_state:
                            st.session_state.carrinhos_ativos = []
                        if cliente.id not in st.session_state.carrinhos_ativos:
                            st.session_state.carrinhos_ativos.append(cliente.id)
                        st.success(f"Carrinho iniciado para {cliente.nome}")
                        st.rerun()
                    if st.button("Editar", key=f"edit_{cliente.id}"):
                        st.session_state.editing_client = cliente.id
                    if st.button("Deletar", key=f"del_{cliente.id}"):
                        if delete_cliente(db, cliente.id):
                            st.success("Cliente deletado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao deletar cliente.")
        
        # Formulário de edição
        if 'editing_client' in st.session_state:
            st.header("Editar Cliente")
            cliente = next((c for c in clientes if c.id == st.session_state.editing_client), None)
            if cliente:
                with st.form("editar_cliente"):
                    nome = st.text_input("Nome", value=cliente.nome)
                    endereco = st.text_input("Endereço", value=cliente.endereco)
                    telefone = st.text_input("Telefone", value=cliente.telefone)
                    email = st.text_input("Email", value=cliente.email)
                    if st.form_submit_button("Atualizar Cliente"):
                        if update_cliente(db, cliente.id, nome, endereco, telefone, email):
                            st.success("Cliente atualizado com sucesso!")
                            del st.session_state.editing_client
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar cliente.")
        
        db.close()
if st.sidebar.button("Ir para Carrinhos"):
        st.session_state.page = "carrinhos"
        st.rerun()

if not_authenticated():
    st.stop()
else:
    cliente_page()
