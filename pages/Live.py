import streamlit as st
from utils.cache import get_cached_matches


def is_live(status: str) -> bool:
    if not status:
        return False

    status = status.lower()

    return any(x in status for x in ["need", "requires", "balls", "overs"])


def show():
    st.title("🏏 Live Matches")

    matches = get_cached_matches()

    if not matches:
        st.warning("No matches available")
        return

    live_found = False

    for m in matches:
        try:
            status = m.get("status", "")

            if not is_live(status):
                continue

            live_found = True

            teams = m.get("teams", ["Team A", "Team B"])
            score = m.get("score", [])

            t1_score = "N/A"
            t2_score = "N/A"

            if isinstance(score, list) and len(score) > 0:
                t1_score = f"{score[0].get('r',0)}/{score[0].get('w',0)} ({score[0].get('o',0)} ov)"

            if isinstance(score, list) and len(score) > 1:
                t2_score = f"{score[1].get('r',0)}/{score[1].get('w',0)} ({score[1].get('o',0)} ov)"

            st.markdown("---")

            col1, col2, col3 = st.columns([3,1,3])

            with col1:
                st.subheader(f"🔴 {teams[0]}")
                st.write(f"Score: {t1_score}")

            with col2:
                st.markdown("### VS")

            with col3:
                st.subheader(f"🔴 {teams[1]}")
                st.write(f"Score: {t2_score}")

            st.write(f"Venue: {m.get('venue','N/A')}")
            st.write(f"Status: {status}")

        except Exception as e:
            st.error(f"Error: {e}")

    if not live_found:
        st.info("No live matches currently")