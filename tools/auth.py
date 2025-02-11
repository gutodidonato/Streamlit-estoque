import streamlit as st
from db import get_user_auth, create_user, get_users, get_db, SessionLocal, get_user_by_username, get_users
import time
from tools.smtp import enviar_mensagem_admin

def registrar() -> bool | None:
    usuarios = get_users()
    if not usuarios:
        if st.button(label=":blue[Registrar]"):
            st.session_state.registro = not st.session_state.registro 
            return
    else:
        rec_senha = st.button(":blue[Recuperar Senha]")
        if rec_senha:
            if enviar_mensagem_admin():
               return True 
            
    

                
def login(username, password):
    if st.button(":blue[Login]"):
        try:
            if get_user_auth(username=username, password=password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['username_id'] = get_user_by_username(username=username)
                st.success("Login realizado com sucesso!")
                time.sleep(3)
                st.rerun()
            else:
                st.error("Credenciais inválidas")
        except Exception as e:
                print(e)                
                st.error("Usuário ou senha incorretos.")
                
def not_authenticated():
    if 'registro' not in st.session_state:
        st.session_state.registro = False
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.title("App com Autenticação")
        st.write("Por favor, faça login para continuar.")
        
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            login(username, password)  
        
        with col2:
            registro = registrar() 
        if registro:
            st.success("Email de recuperação Enviado! ")
            time.sleep(7)
            st.rerun()
             
            
            
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
                    st.write('Conta criada com sucesso')
                    time.sleep(3)
                    st.rerun()
                except Exception as e:
                    print("Log:", e)
        
        return True
    else:
        return False

    
    