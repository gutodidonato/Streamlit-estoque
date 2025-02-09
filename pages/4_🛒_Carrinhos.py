import datetime
import streamlit as st
from db import SessionLocal, get_cliente, get_carrinho_by_cliente, get_itens_by_carrinho, add_item_to_carrinho, remove_item_from_carrinho, get_produtos, create_venda, get_vendedor_by_nome, update_item_carrinho
from tools.auth import not_authenticated

def carrinho_page():
    st.title("Gerenciamento de Carrinhos")

    if 'carrinhos_ativos' not in st.session_state or not st.session_state.carrinhos_ativos:
        st.info("Nenhum carrinho ativo. Inicie um carrinho na página de clientes.")
        if st.button("Voltar para Clientes", key="voltar_clientes"):
            st.session_state.page = "clientes"
            st.rerun()
        return


    cliente_names = [get_cliente(client_id).nome for client_id in st.session_state.carrinhos_ativos]
    
    selected_cliente = st.selectbox("Selecione o cliente:", cliente_names)
    cliente_id = st.session_state.carrinhos_ativos[cliente_names.index(selected_cliente)]
    exibir_carrinho(cliente_id)

    if st.sidebar.button("Voltar para Clientes", key="sidebar_voltar_clientes"):
        st.session_state.page = "clientes"
        st.rerun()

def exibir_carrinho(cliente_id):
    cliente = get_cliente(cliente_id)
    carrinho = get_carrinho_by_cliente(cliente_id)
    
    st.header(f"Carrinho de {cliente.nome}")
    
    col1, col2 = st.columns(2)
    with col1:
        check_taxa = st.checkbox('Terá custo de entrega?', key=f'taxa_{cliente_id}')
    with col2:
        check_vendedor = st.checkbox('Foi atendido?', key=f'vendedor_{cliente_id}')
    
    if check_taxa:
        entrega = st.number_input('Custo de Entrega', min_value=0.0, step=0.1, key=f'entrega_{cliente_id}')
    if check_vendedor:
        vendedor = st.text_input('Nome do vendedor', key=f'nome_vendedor_{cliente_id}')
    
    st.markdown("---")
    
    if carrinho:
        itens = get_itens_by_carrinho(carrinho.id)
        if itens:
            total = 0
            for item in itens:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{item.produto.nome}**")
                with col2:
                    st.write(f"Qtd: {item.quantidade}")
                with col3:
                    subtotal = item.produto.preco_atual * item.quantidade
                    st.write(f"R$ {subtotal:.2f}")
                    total += subtotal
                
                with st.expander("Opções", expanded=False):
                    nova_quantidade = st.number_input("Nova quantidade", min_value=1, value=item.quantidade, key=f"qtd_{item.id}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Atualizar quantidade", key=f"update_{item.id}"):
                            update_item_carrinho(item.id, nova_quantidade)
                            st.success("Quantidade atualizada!")
                            st.rerun()
                    with col2:
                        if st.button("Remover item", key=f"remove_{item.id}"):
                            if remove_item_from_carrinho(cliente.id, item.produto_id):
                                st.success(f"{item.produto.nome} removido do carrinho!")
                                st.rerun()
                            else:
                                st.error("Erro ao remover item do carrinho.")
                
                st.markdown("---")
            
            st.markdown(f"### Total: R$ {total:.2f}")
            
            if check_taxa:
                total += entrega
                st.markdown(f"### Total com entrega: R$ {total:.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Finalizar Compra", key=f"finish_{carrinho.id}"):
                    if check_vendedor and not vendedor:
                        st.error("Por favor, insira o nome do vendedor.")
                    else:
                        vendedor_id = get_vendedor_by_nome(vendedor) if check_vendedor else None
                        user_id = st.session_state.get('username_id')
                        
                        create_venda(
                            vendedor_id,
                            cliente_id,
                            carrinho.id,
                            total,
                            entrega if check_taxa else 0,
                            datetime.now()
                        )
                        
                        st.success("Compra finalizada com sucesso!")
                        st.session_state.carrinhos_ativos.remove(cliente_id)
                        st.rerun()
            with col2:
                if st.button("Cancelar Carrinho", key=f"cancel_{carrinho.id}"):
                    if st.confirm("Tem certeza que deseja cancelar este carrinho?"):
                        # Aqui você pode adicionar a lógica para cancelar o carrinho
                        # Por exemplo, remover todos os itens e o próprio carrinho do banco de dados
                        st.session_state.carrinhos_ativos.remove(cliente_id)
                        st.success("Carrinho cancelado com sucesso!")
                        st.rerun()
        else:
            st.info("O carrinho está vazio.")
    else:
        st.warning("Carrinho não encontrado.")

if not_authenticated():
    st.stop()
else:
    carrinho_page()