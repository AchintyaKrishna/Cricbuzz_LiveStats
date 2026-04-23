import requests

API_KEY = "43523bfda8msh3c00f7d97d09d73p124f4ajsn15b32b4b6bf9"

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1"


def get_overs_data(match_id: str):
    url = f"{BASE_URL}/{match_id}/overs"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
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