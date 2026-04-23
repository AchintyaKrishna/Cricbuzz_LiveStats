import requests
import os
import streamlit as st
from typing import List, Dict, Any


def get_headers() -> Dict[str, str]:
    api_key = os.getenv("RAPIDAPI_KEY") or st.secrets.get("RAPIDAPI_KEY")
    if not api_key:
        raise ValueError("RAPIDAPI_KEY not found")
    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }


def extract_team_score(score_data: Dict[str, Any], team_key: str) -> Dict[str, Any]:
    try:
        innings = score_data.get(team_key, {}).get("inngs1", {})
        return {
            "runs": innings.get("runs", 0),
            "wickets": innings.get("wickets", 0),
            "overs": float(innings.get("overs", 0))
        }
    except Exception:
        return {"runs": 0, "wickets": 0, "overs": 0}


def get_live_matches() -> List[Dict[str, Any]]:
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()
        matches = []

        for t in data.get("typeMatches", []):
            for series in t.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper")
                if not wrapper:
                    continue

                for match in wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})

                    team1 = info.get("team1", {}).get("teamName", "N/A")
                    team2 = info.get("team2", {}).get("teamName", "N/A")

                    t1_score = extract_team_score(score, "team1Score")
                    t2_score = extract_team_score(score, "team2Score")

                    matches.append({
                        "match_id": info.get("matchId"),
                        "match_desc": info.get("matchDesc", "N/A"),
                        "match_type": info.get("matchFormat", "N/A"),
                        "status": info.get("status", "N/A"),
                        "venue": info.get("venueInfo", {}).get("ground", "N/A"),
                        "date": info.get("startDate"),
                        "team1": team1,
                        "team2": team2,
                        "team1_score": t1_score,
                        "team2_score": t2_score
                    })

        return matches

    except Exception:
        return []