import sqlite3
from api.cricket_api import get_live_matches


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id TEXT PRIMARY KEY,
        team1 TEXT,
        team2 TEXT,
        team1_runs INTEGER,
        team1_wickets INTEGER,
        team1_overs REAL,
        team2_runs INTEGER,
        team2_wickets INTEGER,
        team2_overs REAL,
        status TEXT,
        venue TEXT,
        date TEXT
    )
    """)


def run_pipeline():
    conn = sqlite3.connect("database/cricket.db")
    cursor = conn.cursor()

    create_table(cursor)

    matches = get_live_matches()

    if not matches:
        print("No matches found")
        return

    for i, match in enumerate(matches):

        teams = match.get("teams", [])

        if len(teams) < 2:
            continue

        match_id = match.get("id", f"match_{i}")

        team1 = teams[0]
        team2 = teams[1]

        score = match.get("score", [])

        t1_runs = score[0].get("r", 0) if len(score) > 0 else 0
        t1_wickets = score[0].get("w", 0) if len(score) > 0 else 0
        t1_overs = score[0].get("o", 0) if len(score) > 0 else 0

        t2_runs = score[1].get("r", 0) if len(score) > 1 else 0
        t2_wickets = score[1].get("w", 0) if len(score) > 1 else 0
        t2_overs = score[1].get("o", 0) if len(score) > 1 else 0

        cursor.execute("""
            INSERT OR REPLACE INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match_id,
            team1,
            team2,
            t1_runs,
            t1_wickets,
            t1_overs,
            t2_runs,
            t2_wickets,
            t2_overs,
            match.get("status"),
            match.get("venue"),
            match.get("date")
        ))

    conn.commit()
    conn.close()

    print("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()