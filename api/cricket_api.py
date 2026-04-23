import requests

API_KEY = "43523bfda8msh3c00f7d97d09d73p124f4ajsn15b32b4b6bf9"

BASE_URL = "https://cricket-live-line-advance.p.rapidapi.com/competitions/129438/matches?paged=1&per_page=50"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricket-live-line-advance.p.rapidapi.com"
}


def get_live_matches():
    url = f"{BASE_URL}/matches"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        data = res.json()

        if data.get("status") != "ok":
            print("API returned error")
            return []

        matches = []

        items = data.get("response", {}).get("items", [])

        for m in items:
            try:
                team1 = m.get("teama", {}).get("name", "Team A")
                team2 = m.get("teamb", {}).get("name", "Team B")

                score1_raw = m.get("teama", {}).get("scores", "")
                score2_raw = m.get("teamb", {}).get("scores", "")

                overs1 = m.get("teama", {}).get("overs", "0")
                overs2 = m.get("teamb", {}).get("overs", "0")

                # ---------- SAFE SCORE PARSE ----------
                def parse_score(score):
                    try:
                        if "/" in score:
                            r, w = score.split("/")
                            return int(r), int(w)
                        return 0, 0
                    except:
                        return 0, 0

                r1, w1 = parse_score(score1_raw)
                r2, w2 = parse_score(score2_raw)

                match_data = {
                    "id": m.get("match_id"),
                    "name": m.get("title"),
                    "matchType": m.get("format_str"),
                    "status": m.get("status_str"),
                    "venue": m.get("venue", {}).get("name", ""),
                    "date": m.get("date_start_ist"),

                    "teams": [team1, team2],

                    # ✅ IMPORTANT (used in your app)
                    "score": [
                        {"r": r1, "w": w1, "o": float(overs1) if overs1 else 0},
                        {"r": r2, "w": w2, "o": float(overs2) if overs2 else 0}
                    ]
                }

                matches.append(match_data)

            except Exception as e:
                print("Error parsing match:", e)
                continue

        return matches

    except Exception as e:
        print("API ERROR:", e)
        return []