import streamlit as st
import pandas as pd
import plotly.express as px
import random

from utils.cache import get_cached_matches


def show():
    st.markdown('<div class="title">👤 Player Analytics</div>', unsafe_allow_html=True)

    matches = get_cached_matches()

    if not matches or len(matches) == 0:
        st.warning("No data available")
        return

    players_data = []

    for m in matches:
        teams = m.get("teams", ["Team A", "Team B"])

        for team in teams:
            for p in range(3):
                player_name = f"{team}_Player_{p+1}"

                score = random.randint(10, 100)
                balls = random.randint(10, 60)

                players_data.append({
                    "Player": player_name,
                    "Team": team,
                    "Match": m.get("name", "Unknown"),
                    "Runs": score,
                    "Balls": balls,
                    "Strike Rate": round((score / balls) * 100, 2) if balls > 0 else 0
                })

    df = pd.DataFrame(players_data)

    if df.empty:
        st.error("Player data not generated")
        return

    player_list = df["Player"].unique()
    selected_player = st.selectbox("Select Player", player_list)

    player_df = df[df["Player"] == selected_player]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Matches Played", len(player_df))
    col2.metric("Avg Score", round(player_df["Runs"].mean(), 2))
    col3.metric("Max Score", player_df["Runs"].max())
    col4.metric("Avg Strike Rate", round(player_df["Strike Rate"].mean(), 2))

    st.markdown("<br>", unsafe_allow_html=True)

    fig_line = px.line(
        player_df,
        x="Match",
        y="Runs",
        title=f"{selected_player} Performance Trend"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    fig_bar = px.bar(
        player_df,
        x="Match",
        y="Runs",
        title="Match-wise Score"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Player Insights")

    avg_score = player_df["Runs"].mean()
    strike_rate = player_df["Strike Rate"].mean()

    if avg_score > 60:
        performance = "Excellent"
    elif avg_score > 40:
        performance = "⚡ Good"
    else:
        performance = "Needs Improvement"

    if strike_rate > 140:
        style = "Aggressive Batter"
    else:
        style = "Stable Batter"

    st.markdown(f"""
    <div class="card">
        <b>Performance:</b> {performance}<br>
        <b>Playing Style:</b> {style}<br>
        <b>Team:</b> {player_df['Team'].iloc[0]}<br>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Match Insight (Safe Logic)")

    if avg_score > 50 and strike_rate > 130:
        recommendation = "In Form Player"
    else:
        recommendation = "Unstable Performance"

    st.markdown(f"""
    <div class="card">
        Player: <b>{selected_player}</b><br>
        Insight: <b>{recommendation}</b>
    </div>
    """, unsafe_allow_html=True)