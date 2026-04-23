import streamlit as st
from api.cricket_api import get_live_matches

@st.cache_data(ttl=60, show_spinner="Fetching live matches...")
def get_cached_matches():
    return get_live_matches()