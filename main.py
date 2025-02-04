import streamlit as st
from tools.auth import not_authenticated
from db.main import init_db

def main():
    if not_authenticated():
        st.stop() 
    st.write(f"Bem-vindo, {st.session_state['username']}!")

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado.")
    main()
    
    
    