queries = {
    "Top Run Scorers": """
        SELECT name, runs FROM players
        ORDER BY runs DESC LIMIT 10;
    """,

    "Top Wicket Takers": """
        SELECT name, wickets FROM players
        ORDER BY wickets DESC LIMIT 10;
    """,

    "Players by Team": """
        SELECT team, COUNT(*) as total_players
        FROM players GROUP BY team;
    """,

    "All Players": """
        SELECT * FROM players;
    """
}