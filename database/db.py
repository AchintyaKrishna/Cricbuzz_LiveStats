import sqlite3

DB_PATH = "database/cricket.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        team TEXT,
        role TEXT,
        runs INTEGER,
        wickets INTEGER
    )
    """)

    conn.commit()
    conn.close()