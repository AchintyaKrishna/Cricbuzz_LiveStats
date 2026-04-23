import requests
import os
import streamlit as st
from typing import List, Dict, Any


def get_headers():
    api_key = os.getenv("RAPIDAPI_KEY") or st.secrets.get("RAPIDAPI_KEY")
    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-line-advance.p.rapidapi.com"
    }


def get_live_matches() -> List[Dict[str, Any]]:
    url = "https://cricket-live-line-advance.p.rapidapi.com/competitionMatches"

    try:
        headers = get_headers()
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return []

        data = res.json()

        matches = []

        items = data.get("response", {}).get("items", [])

        for match in items:
            short_title = match.get("short_title", "")
            teams = short_title.split(" vs ") if " vs " in short_title else ["", ""]

            matches.append({
                "match_id": match.get("match_id"),
                "match_desc": match.get("title"),
                "match_type": match.get("format_str"),
                "status": match.get("status_str"),
                "venue": match.get("subtitle"),
                "date": match.get("date_start"),
                "team1": teams[0],
                "team2": teams[1] if len(teams) > 1 else "",
                "team1_score": {},
                "team2_score": {}
            })

        return matches

    except Exception:
        return []