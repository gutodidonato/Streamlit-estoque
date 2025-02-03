import streamlit as st

def authenticate(username, password):
    users = [
        {
            "username": "admin",
            "password": "admin"
        }
    ]
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def not_authenticated():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.title("App com Autenticação")
        st.write("Por favor, faça login para continuar.")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
        return True
    else:
        return False 
    
def first_user():
    users = []
    if not user in users:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        st.button("Criar conta")
        users.append({"username": user, "password": password})