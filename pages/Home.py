import streamlit as st
import pandas as pd
import plotly.express as px
from utils.cache import get_cached_matches

def clean_status(status: str) -> str:
    if not status:
        return "Other"

    status = status.lower()

    if any(x in status for x in ["won", "beat", "defeated"]):
        return "Completed"
    elif any(x in status for x in ["need", "requires", "balls", "overs"]):
        return "Live"
    elif any(x in status for x in ["opt", "toss", "elected"]):
        return "Upcoming"
    else:
        return "Other"


def show():

    st.markdown('<div class="title">📊 Cricket Match Insights Dashboard</div>', unsafe_allow_html=True)

    matches = get_cached_matches()

    if not matches:
        st.warning("No data available from API")
        return

    data = []

    for m in matches:
        try:
            teams = m.get("teams", ["Team A", "Team B"])
            raw_status = m.get("status", "Unknown")

            data.append({
                "Match": m.get("name", "Unknown"),
                "Team1": teams[0],
                "Team2": teams[1],
                "Type": m.get("matchType", "Unknown"),
                "Status": clean_status(raw_status),
                "RawStatus": raw_status,
                "Venue": m.get("venue", "Unknown")
            })

        except:
            continue

    df = pd.DataFrame(data)

    live_count = len(df[df["Status"] == "Live"])

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Matches", len(df))
    col2.metric("Live Matches", live_count)  
    col3.metric("Teams", len(set(df["Team1"]).union(set(df["Team2"]))))
    col4.metric("Match Types", df["Type"].nunique())
    col5.metric("Venues", df["Venue"].nunique())

    if live_count == 0:
        st.info("No live matches right now. Showing recent & upcoming matches.")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    type_count = df["Type"].value_counts().reset_index()
    type_count.columns = ["Type", "Count"]

    if len(type_count) == 1:
        st.info(f"Only {type_count.iloc[0]['Type']} matches available currently")

    fig1 = px.bar(
        type_count,
        x="Type",
        y="Count",
        title="Match Type Distribution"
    )
    col1.plotly_chart(fig1, use_container_width=True)

    status_count = df["Status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]

    fig2 = px.pie(
        status_count,
        names="Status",
        values="Count",
        title="Match Status Distribution",
        hole=0.4
    )
    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📋 All Matches")

    for row in data:
        st.markdown(f"""
        <div class="card">
            <h4>{row['Match']}</h4>
            <p>{row['Team1']} vs {row['Team2']}</p>
            <p><b>Status:</b> {row['RawStatus']}</p>
            <p><b>Venue:</b> {row['Venue']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- LIVE SECTION ----------
    st.subheader("🔴 Live Matches")

    live_df = df[df["Status"] == "Live"]

    if not live_df.empty:
        for _, row in live_df.iterrows():
            st.markdown(f"""
            <div class="card">
                <h4>{row['Match']}</h4>
                <p>{row['Team1']} vs {row['Team2']}</p>
                <p><b>Status:</b> {row['RawStatus']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No live matches currently")