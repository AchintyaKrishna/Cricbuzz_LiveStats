import requests

def get_api_key():
    key = os.getenv("RAPIDAPI_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["RAPIDAPI_KEY"]
    except:
        return None

API_KEY = get_api_key()

BASE_URL = "https://cricket-live-line-advance.p.rapidapi.com/competitions/129438/matches?paged=1&per_page=50"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricket-live-line-advance.p.rapidapi.com"
}

    try:
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return []

        data = res.json()

        overs = data.get("overs", [])

        clean_data = []

        for o in overs:
            clean_data.append({
                "overnum": o.get("overnum", 0),
                "runs": o.get("runs", 0),
                "score": o.get("score", 0),
                "runrate": o.get("runrate", 0),
                "wickets": o.get("wickets", 0)
            })

        return clean_data

    except:
        return []
