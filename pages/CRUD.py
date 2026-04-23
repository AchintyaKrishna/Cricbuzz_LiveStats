import streamlit as st
import pandas as pd
from database.db import get_connection


def show():
    st.markdown('<div class="title">🛠 Player Management (Production CRUD)</div>', unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_sql("SELECT * FROM players", conn)

    total_players = len(df)
    total_runs = df["runs"].sum() if not df.empty else 0
    total_wickets = df["wickets"].sum() if not df.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Players", total_players)
    col2.metric("Total Runs", total_runs)
    col3.metric("Total Wickets", total_wickets)

    st.divider()

    st.subheader("Add Player")

    name = st.text_input("Name")
    team = st.text_input("Team")
    role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder"])
    runs = st.number_input("Runs", min_value=0)
    wickets = st.number_input("Wickets", min_value=0)

    if st.button("Add Player"):
        if name and team:
            cursor.execute(
                "INSERT INTO players (name, team, role, runs, wickets) VALUES (?, ?, ?, ?, ?)",
                (name, team, role, runs, wickets)
            )
            conn.commit()
            st.success("Player added!")
            st.rerun()
        else:
            st.warning("Fill all fields")

    st.divider()

    st.subheader("Player List")

    df = pd.read_sql("SELECT * FROM players", conn)

    if df.empty:
        st.info("No players found")
    else:
        search = st.text_input("Search Player")

        if search:
            df = df[df["name"].str.contains(search, case=False)]

        st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("Delete Player")

    df = pd.read_sql("SELECT * FROM players", conn)

    if not df.empty:
        player_names = df["name"].tolist()

        selected = st.selectbox("Select Player", player_names)

        if st.button("Delete"):
            cursor.execute("DELETE FROM players WHERE name = ?", (selected,))
            conn.commit()
            st.success(f"{selected} deleted")
            st.rerun()

    st.divider()

    st.subheader("Update Player")

    df = pd.read_sql("SELECT * FROM players", conn)

    if not df.empty:
        selected = st.selectbox("Select Player to Update", df["name"].tolist())

        player = df[df["name"] == selected].iloc[0]

        new_runs = st.number_input("Runs", value=int(player["runs"]))
        new_wickets = st.number_input("Wickets", value=int(player["wickets"]))

        if st.button("Update"):
            cursor.execute(
                "UPDATE players SET runs=?, wickets=? WHERE name=?",
                (new_runs, new_wickets, selected)
            )
            conn.commit()
            st.success("Player updated!")
            st.rerun()

    conn.close()