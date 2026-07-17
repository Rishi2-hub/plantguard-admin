import streamlit as st

def topbar():

    col1, col2 = st.columns([5,1])

    with col1:
        st.title("PlantGuard Admin Dashboard")

    with col2:
        st.success("Admin")