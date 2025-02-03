import streamlit as st
from tools.auth import not_authenticated

def main():
    if not_authenticated():
        st.stop() 
    st.write(f"Bem-vindo, {st.session_state['username']}!")

if __name__ == "__main__":
    main()
    
    
    