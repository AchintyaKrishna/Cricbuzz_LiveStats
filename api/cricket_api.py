import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://cricbuzz-cricket2.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket2.p.rapidapi.com"
}


def get_live_matches():
    url = f"{BASE_URL}/matches/v1/live"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        data = res.json()

        matches = []

        for t in data.get("typeMatches", []):
            for series in t.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper")

                if not wrapper:
                    continue

                for match in wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})

                    team1 = info.get("team1", {}).get("teamName", "")
                    team2 = info.get("team2", {}).get("teamName", "")

                    # ---------- SCORE ----------
                    def extract_team_score(team):
                        try:
                            innings = score.get(team, {}).get("inngs1", {})
                            return {
                                "r": innings.get("runs", 0),
                                "w": innings.get("wickets", 0),
                                "o": float(innings.get("overs", 0))
                            }
                        except:
                            return {"r": 0, "w": 0, "o": 0}

                    t1_score = extract_team_score("team1Score")
                    t2_score = extract_team_score("team2Score")

                    matches.append({
                        "id": info.get("matchId"),
                        "name": info.get("matchDesc"),
                        "matchType": info.get("matchFormat"),
                        "status": info.get("status"),
                        "venue": info.get("venueInfo", {}).get("ground", ""),
                        "date": info.get("startDate"),
                        "teams": [team1, team2],
                        "score": [t1_score, t2_score]
                    })

        return matches

    except Exception as e:
        print("API ERROR:", e)
        return []