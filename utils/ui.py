import streamlit as st

def load_ui():
    st.set_page_config(layout="wide")

    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg,#0f172a,#020617);
        color:white;
    }

    .title {
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(90deg,#22c55e,#06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .card {
        background: rgba(255,255,255,0.05);
        padding:20px;
        border-radius:15px;
        border:1px solid rgba(255,255,255,0.1);
        margin-bottom:15px;
    }

    </style>
    """, unsafe_allow_html=True)