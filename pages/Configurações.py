from tools.auth import not_authenticated
import streamlit as st

if not_authenticated():
    st.stop()
st.write("Rodar app")    