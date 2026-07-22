import streamlit as st
from components.radar_chart import render_radar_figure
from lib.claude import fetch_live_signals


def _score_color(score):
    if score >= 70:
        return "#34d399"
    if score >= 45:
        return "#fbbf24"
    return "#f87171"


def _strength_color(s):
    v = (s or "").lower()
    if v.startswith("h"):
        return "#34d399"
    if v.startswith("m"):
        return "#fbbf24"
    return "#9c98a8"


def _render_live_signals(record, idx, on_update):
    st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("<h3>🔎 Live customer signals</h3>", unsafe_allow_html=True)

    live = record.get("liveSignals")

    def run_search():
        with st.spinner("Searching Reddit, Hacker News, and niche communities…"):
            try:
                data = fetch_live_signals(record["idea"], record.get("problem", ""))
                record["liveSignals"] = data
                on_update(data)
            except Exception as e:
                st.session_state[f"live_signals_error_{idx}"] = str(e)

    if live is None and f"live_signals_error_{idx}" not in st.session_state:
        run_search()
        live = record.get("liveSignals")
        st.rerun()

    with top_col2:
        if st.button("Refresh", key=f"refresh_signals_{idx}", use_container_width=True):
            st.session_state.pop(f"live_signals_error_{idx}", None)
            record["liveSignals"] = None
            st.rerun()

    if f"live_signals_error_{idx}" in st.session_state:
        st.caption("Couldn't complete the live search right now.")
        if st.button("Try again", key=f"retry_signals_{idx}"):
            st.session_state.pop(f"live_signals_error_{idx}", None)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if live:
        score = live.get("signalScore", 0)
        color = _score_color(score)
        st.markdown(
            f'<span class="fiq-pill" style="color:{color};border-color:{color}55;background:{color}18;">'
            f"{score} demand signal</span>",
            unsafe_allow_html=True,
        )
        threads = live.get("threads", [])
        if not threads:
            st.markdown(
                f"<p style='color:var(--muted);font-size:13.5px;margin-top:10px;'>"
                f"{live.get('signalSummary', 'No strong real-world discussions found yet.')}</p>",
                unsafe_allow_html=True,
            )
        else:
            if live.get("signalSummary"):
                st.markdown(
                    f"<p style='color:var(--muted);font-size:13.5px;margin-top:10px;'>{live['signalSummary']}</p>",
                    unsafe_allow_html=True,
                )
            for t in threads:
                c = _strength_color(t.get("strength"))
                url_html = (
                    f'<a href="{t["url"]}" target="_blank" style="color:var(--purple-2);font-size:12.5px;">View discussion →</a>'
                    if t.get("url") else ""
                )
                st.markdown(
                    f"""
                    <div class="fiq-thread">
                      <div class="top">
                        <span class="fiq-platform-tag">{t.get('platform', 'Web')}</span>
                        <span class="fiq-strength-tag" style="color:{c};border-color:{c}55;background:{c}18;">{t.get('strength', 'Signal')}</span>
                      </div>
                      <div class="title">{t.get('title', '')}</div>
                      <p class="insight">{t.get('insight', '')}</p>
                      {'<p class="fiq-reply"><strong>Reply angle:</strong> ' + t.get('replyAngle', '') + '</p>' if t.get('replyAngle') else ''}
                      {url_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    st.markdown("</div>", unsafe_allow_html=True)


def render_report(record, idx, on_back, on_update_live_signals):
    if st.button("← Back to dashboard"):
        on_back()
        return

    r = record["report"]
    color = _score_color(r["overallScore"])

    head_col1, head_col2 = st.columns([1, 4])
    with head_col1:
        st.markdown(
            f"""<div class="fiq-score-circle" style="background:{color}22;border:2px solid {color}55;">
            <span class="num" style="color:{color};">{r['overallScore']}</span>
            <span class="lbl">Score</span></div>""",
            unsafe_allow_html=True,
        )
    with head_col2:
        st.markdown(f"### {record['idea']}")
        st.caption(r.get("verdict", ""))

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>📊 Radar scoring</h3>", unsafe_allow_html=True)
        st.plotly_chart(render_radar_figure(r.get("radar", {})), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>📝 Executive summary</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{r.get('executiveSummary', '')}</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:18px;'>🌍 Market analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{r.get('marketAnalysis', '')}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>🏟️ Competitive landscape</h3>", unsafe_allow_html=True)
        for c in r.get("competitors", []):
            st.markdown(
                f"""<div class="fiq-competitor"><div class="name">{c['name']}</div>
                <div class="detail"><strong style="color:#86efac;">+</strong> {c['strength']}<br>
                <strong style="color:#fca5a5;">–</strong> {c['weakness']}</div></div>""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>🧩 SWOT analysis</h3>", unsafe_allow_html=True)
        swot = r.get("swot", {})
        sw_col1, sw_col2 = st.columns(2)
        with sw_col1:
            items = "".join(f"<li>{s}</li>" for s in swot.get("strengths", []))
            st.markdown(f'<div class="fiq-swot-box"><h4 style="color:#86efac;">Strengths</h4><ul>{items}</ul></div>', unsafe_allow_html=True)
            items = "".join(f"<li>{s}</li>" for s in swot.get("opportunities", []))
            st.markdown(f'<div class="fiq-swot-box"><h4 style="color:#93c5fd;">Opportunities</h4><ul>{items}</ul></div>', unsafe_allow_html=True)
        with sw_col2:
            items = "".join(f"<li>{s}</li>" for s in swot.get("weaknesses", []))
            st.markdown(f'<div class="fiq-swot-box"><h4 style="color:#fca5a5;">Weaknesses</h4><ul>{items}</ul></div>', unsafe_allow_html=True)
            items = "".join(f"<li>{s}</li>" for s in swot.get("threats", []))
            st.markdown(f'<div class="fiq-swot-box"><h4 style="color:#fcd34d;">Threats</h4><ul>{items}</ul></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>🎯 Target customer</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{r.get('targetCustomer', '')}</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:18px;'>💰 Revenue model</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{r.get('revenueModel', {}).get('suggested', '')}</p>", unsafe_allow_html=True)
        items = "".join(f"<li>{s}</li>" for s in r.get("revenueModel", {}).get("pricingIdeas", []))
        st.markdown(f"<ul>{items}</ul>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>🚀 Go-to-market strategy</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{r.get('gtmStrategy', '')}</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:18px;'>⚠️ Risks &amp; mitigations</h3>", unsafe_allow_html=True)
        for x in r.get("risks", []):
            st.markdown(
                f'<div class="fiq-risk"><div class="t">{x["risk"]}</div><div class="m">{x["mitigation"]}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>📣 Customer discovery channels</h3>", unsafe_allow_html=True)
        for c in r.get("outreachChannels", []):
            st.markdown(f"**{c['channel']}**")
            st.code(c["template"], language=None)  # built-in copy button
        st.markdown("</div>", unsafe_allow_html=True)
    with col8:
        st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)
        st.markdown("<h3>✅ Execution checklist</h3>", unsafe_allow_html=True)
        checklist = r.get("executionChecklist", [])
        done = record.setdefault("checklistDone", [False] * len(checklist))
        while len(done) < len(checklist):
            done.append(False)
        changed = False
        for i, step in enumerate(checklist):
            checked = st.checkbox(step, value=done[i], key=f"check_{idx}_{i}")
            if checked != done[i]:
                done[i] = checked
                changed = True
        if changed:
            on_update_live_signals(record.get("liveSignals"))  # triggers a save of the whole record
        completed = sum(done)
        if checklist:
            st.progress(completed / len(checklist))
            st.caption(f"{completed}/{len(checklist)} steps complete")
        st.markdown("</div>", unsafe_allow_html=True)

    _render_live_signals(record, idx, lambda data: on_update_live_signals(data))
