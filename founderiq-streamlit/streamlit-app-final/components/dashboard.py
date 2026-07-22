import streamlit as st
from datetime import datetime


def _score_color(score):
    if score >= 70:
        return "#34d399"
    if score >= 45:
        return "#fbbf24"
    return "#f87171"


def render_dashboard(ideas, on_new_idea, on_view_report):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Your ideas")
        st.caption(f"{len(ideas)} idea{'s' if len(ideas) != 1 else ''} validated so far.")
    with col2:
        if st.button("✨ Validate a new idea", use_container_width=True, type="primary"):
            on_new_idea()

    st.write("")

    if not ideas:
        st.markdown(
            """
            <div class="fiq-panel" style="text-align:center;padding:50px 20px;">
              <div style="font-size:32px;margin-bottom:10px;">✨</div>
              <h3 style="margin:0 0 6px;">No ideas validated yet</h3>
              <p>Describe a B2B idea and get a full VC-grade report in seconds.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for idx in reversed(range(len(ideas))):
        it = ideas[idx]
        color = _score_color(it["report"]["overallScore"])
        date_str = datetime.fromtimestamp(it["createdAt"]).strftime("%b %d, %Y")
        row_col1, row_col2 = st.columns([5, 1])
        with row_col1:
            st.markdown(
                f"""
                <div class="fiq-idea-row">
                  <h4>{it['idea']}</h4>
                  <p>{date_str} · {it.get('audience') or 'General B2B audience'}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with row_col2:
            st.markdown(
                f"""<div class="fiq-score-circle" style="background:{color}22;border:1px solid {color}55;">
                <span class="num" style="color:{color};">{it['report']['overallScore']}</span></div>""",
                unsafe_allow_html=True,
            )
            if st.button("Open →", key=f"open_{idx}", use_container_width=True):
                on_view_report(idx)
        st.write("")
