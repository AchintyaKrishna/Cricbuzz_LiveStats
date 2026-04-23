import streamlit as st
import pandas as pd
import sqlite3

from utils.cache import get_cached_matches


def show():
    st.markdown('<div class="title">🧠 SQL Analytics (25 Queries)</div>', unsafe_allow_html=True)

    matches = get_cached_matches()

    if not matches:
        st.warning("No data available")
        return

    data = []
    for m in matches:
        try:
            teams = m.get("teams", ["A", "B"])

            if len(teams) < 2:
                continue

            data.append({
                "match_name": m.get("name", "Unknown"),
                "team1": teams[0],
                "team2": teams[1],
                "match_type": m.get("matchType", "Unknown"),
                "status": m.get("status", "Unknown"),
                "venue": m.get("venue", "Unknown")
            })
        except:
            continue

    if len(data) == 0:
        st.error("Data parsing failed")
        return

    df = pd.DataFrame(data)
    conn = sqlite3.connect(":memory:")
    df.to_sql("matches", conn, index=False, if_exists="replace")

    queries = {

    "1. All Teams Appearing": "SELECT DISTINCT team1 FROM matches",

    "2. Recent Matches": "SELECT * FROM matches ORDER BY match_name DESC",

    "3. Top Match Types": """
        SELECT match_type, COUNT(*) as count
        FROM matches GROUP BY match_type ORDER BY count DESC
    """,

    "4. Venues with Most Matches": """
        SELECT venue, COUNT(*) as count
        FROM matches GROUP BY venue ORDER BY count DESC
    """,

    "5. Matches Won": "SELECT * FROM matches WHERE status LIKE '%won%'",

    "6. Count Teams": "SELECT COUNT(DISTINCT team1) FROM matches",

    "7. Match Types": "SELECT DISTINCT match_type FROM matches",

    "8. All Matches": "SELECT * FROM matches",

    "9. Matches per Team1": "SELECT team1, COUNT(*) FROM matches GROUP BY team1",

    "10. Matches per Team2": "SELECT team2, COUNT(*) FROM matches GROUP BY team2",

    "11. Combined Team Frequency": """
        SELECT team1 as team, COUNT(*) FROM matches GROUP BY team1
        UNION
        SELECT team2, COUNT(*) FROM matches GROUP BY team2
    """,

    "12. Matches per Venue": "SELECT venue, COUNT(*) FROM matches GROUP BY venue",

    "13. Match Count by Type": "SELECT match_type, COUNT(*) FROM matches GROUP BY match_type",

    "14. Unique Venues": "SELECT COUNT(DISTINCT venue) FROM matches",

    "15. Unique Teams": "SELECT COUNT(DISTINCT team1) FROM matches",

    "16. Matches with India": """
        SELECT * FROM matches 
        WHERE team1 LIKE '%India%' OR team2 LIKE '%India%'
    """,

    "17. Total Matches": "SELECT COUNT(*) FROM matches",

    "18. Team vs Team": "SELECT team1, team2 FROM matches",

    "19. Venue List": "SELECT DISTINCT venue FROM matches",

    "20. Match Type Ranking": """
        SELECT match_type, COUNT(*) as total 
        FROM matches GROUP BY match_type ORDER BY total DESC
    """,

    "21. Frequent Teams": """
        SELECT team1, COUNT(*) as cnt 
        FROM matches GROUP BY team1 HAVING cnt > 1
    """,

    "22. Popular Venues": """
        SELECT venue, COUNT(*) 
        FROM matches GROUP BY venue HAVING COUNT(*) > 1
    """,

    "23. Status Distribution": """
        SELECT status, COUNT(*) FROM matches GROUP BY status
    """,

    "24. Team Participation": """
        SELECT team1, COUNT(*) + 
        (SELECT COUNT(*) FROM matches m2 WHERE m2.team2 = matches.team1)
        FROM matches GROUP BY team1
    """,

    "25. Dataset Summary": """
        SELECT 
            COUNT(*) as total_matches,
            COUNT(DISTINCT team1) as teams,
            COUNT(DISTINCT venue) as venues
        FROM matches
    """
    }

    # ---------- UI ----------
    st.subheader("📊 Run SQL Queries")

    selected = st.selectbox("Choose Query", list(queries.keys()))

    if st.button("Execute"):
        result = pd.read_sql(queries[selected], conn)
        st.dataframe(result)

    # ---------- CUSTOM ----------
    st.subheader("🧠 Custom SQL")

    user_query = st.text_area("Write SQL", "SELECT * FROM matches LIMIT 5")

    if st.button("Run Custom"):
        try:
            result = pd.read_sql(user_query, conn)
            st.dataframe(result)
        except Exception as e:
            st.error(e)