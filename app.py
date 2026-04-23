import streamlit as st
from utils.ui import load_ui


from pages import Home, Live, Player, Analytics, SQL_Analytics, CRUD
from database.db import init_db

init_db()

load_ui()

st.markdown("""
<style>
.nav {
    display:flex;
    justify-content:center;
    gap:20px;
    margin-top:20px;
}
.nav button {
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.2);
    padding:10px 20px;
    border-radius:10px;
    color:white;
    cursor:pointer;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

cols = st.columns(6)
pages = ["Home", "Live", "Players", "Analytics", "SQL", "CRUD"]

for i, p in enumerate(pages):
    if cols[i].button(p):
        st.session_state.page = p

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- ROUTING ----------
if st.session_state.page == "Home":
    Home.show()
elif st.session_state.page == "Live":
    Live.show()
elif st.session_state.page == "Players":
    Player.show()
elif st.session_state.page == "Analytics":
    Analytics.show()
elif st.session_state.page == "SQL":
    SQL_Analytics.show()
elif st.session_state.page == "CRUD":
    CRUD.show()