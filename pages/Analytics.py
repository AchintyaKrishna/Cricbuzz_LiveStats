import streamlit as st
import pandas as pd
import plotly.express as px

from utils.cache import get_cached_matches


def extract_score(match, team_index):
    """Extract real score from API response"""
    try:
        score = match.get("score", [])

        if team_index < len(score):
            s = score[team_index]
            runs = s.get("r", 0)
            wickets = s.get("w", 0)
            overs = s.get("o", 1)

            if overs == 0:
                overs = 1

            run_rate = round(runs / overs, 2)

            return runs, wickets, overs, run_rate

        return 0, 0, 1, 0

    except:
        return 0, 0, 1, 0


def show():
    st.markdown('<div class="title">📊 Advanced Team Analytics</div>', unsafe_allow_html=True)

    matches = get_cached_matches()

    if not matches or len(matches) == 0:
        st.warning("No data available (API blocked or empty)")
        return

    data = []

    for m in matches:
        try:
            teams = m.get("teams", ["Team A", "Team B"])

            if len(teams) < 2:
                continue

            runs1, wk1, ov1, rr1 = extract_score(m, 0)
            runs2, wk2, ov2, rr2 = extract_score(m, 1)

            data.append({
                "Match": m.get("name", "Unknown"),
                "Team": teams[0],
                "Opponent": teams[1],
                "Score": runs1,
                "Wickets": wk1,
                "Overs": ov1,
                "Run Rate": rr1
            })

            data.append({
                "Match": m.get("name", "Unknown"),
                "Team": teams[1],
                "Opponent": teams[0],
                "Score": runs2,
                "Wickets": wk2,
                "Overs": ov2,
                "Run Rate": rr2
            })

        except Exception:
            continue

    df = pd.DataFrame(data)

    if df.empty:
        st.error("Data processing failed")
        return

    team_list = df["Team"].unique()
    selected_team = st.selectbox("Select Team", team_list)

    team_df = df[df["Team"] == selected_team]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Score", round(team_df["Score"].mean(), 2))
    col2.metric("Avg Run Rate", round(team_df["Run Rate"].mean(), 2))
    col3.metric("Avg Wickets", round(team_df["Wickets"].mean(), 2))
    col4.metric("Matches Played", len(team_df))

    st.markdown("<br>", unsafe_allow_html=True)

  
    fig_line = px.line(
        team_df,
        x="Match",
        y="Score",
        title=f"{selected_team} Score Trend"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    fig_rr = px.line(
        team_df,
        x="Match",
        y="Run Rate",
        title="Run Rate Trend"
    )
    st.plotly_chart(fig_rr, use_container_width=True)

    fig_bar = px.bar(
        team_df,
        x="Match",
        y="Score",
        title="Score Comparison"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("⚡ Match Dominance")

    dominance_data = []

    for m in matches:
        teams = m.get("teams", ["A", "B"])

        if len(teams) < 2:
            continue

        r1, _, _, _ = extract_score(m, 0)
        r2, _, _, _ = extract_score(m, 1)

        total = r1 + r2 if (r1 + r2) > 0 else 1

        dominance_data.append({
            "Match": m.get("name", "Unknown"),
            teams[0]: round((r1 / total) * 100, 1),
            teams[1]: round((r2 / total) * 100, 1)
        })

    st.dataframe(pd.DataFrame(dominance_data))

    st.subheader("🏆 Win Prediction")

    predictions = []

    for m in matches:
        teams = m.get("teams", ["A", "B"])

        if len(teams) < 2:
            continue

        r1, _, _, _ = extract_score(m, 0)
        r2, _, _, _ = extract_score(m, 1)

        if r1 > r2:
            winner = teams[0]
            prob = 70
        elif r2 > r1:
            winner = teams[1]
            prob = 70
        else:
            winner = "Close Match"
            prob = 50

        predictions.append({
            "Match": m.get("name", "Unknown"),
            "Predicted Winner": winner,
            "Win Probability (%)": prob
        })

    st.dataframe(pd.DataFrame(predictions))

    st.subheader("Team Recommendation")

    for row in predictions:
        st.markdown(f"""
        <div class="card">
            <b>{row['Match']}</b><br>
            Recommended Team: <b>{row['Predicted Winner']}</b><br>
        </div>
        """, unsafe_allow_html=True)