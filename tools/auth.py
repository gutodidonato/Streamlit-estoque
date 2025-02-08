import streamlit as st
from db import get_user_auth, create_user, get_users, get_db, SessionLocal, get_user_by_username

def registrar():
    if 'registro' not in st.session_state:
        st.session_state.registro = False
    if st.button("Registrar"):
        st.session_state.registro = True 

    if st.session_state.registro:
        st.write("Página de registro")
        new_username = st.text_input("Crie seu usuário")
        new_password = st.text_input("Crie sua senha", type="password")
        email = st.text_input("Email")
        if st.button("Efetuar Registro"):
            try:
                create_user(username=new_username, password=new_password, email=email)
                st.session_state['authenticated'] = True
                st.session_state['username'] = new_username
                st.session_state['username_id'] = get_user_by_username(username=new_username)
                st.rerun()
            except:
                st.error("Erro ao criar usuário")
def login(username, password):
    if st.button("Login"):
        try:
            if get_user_auth(username=username, password=password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['username_id'] = get_user_by_username(username=username)
                st.success("Login realizado com sucesso!")
                st.rerun()
        except Exception as e:
                print(e)                
                st.error("Usuário ou senha incorretos.")
                
def not_authenticated():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.title("App com Autenticação")
        st.write("Por favor, faça login para continuar.")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        login(username, password)
        registrar()
                
        return True
    else:
        return False 

    
    
def first_user():
    users = get_users(db=get_db)
    if not user in users:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        st.button("Criar conta")
        users.append({"username": user, "password": password})