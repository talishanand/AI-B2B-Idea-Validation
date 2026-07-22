import time
import streamlit as st

from lib.styles import CUSTOM_CSS
from lib.storage import get_ideas, save_ideas
from lib.claude import validate_idea
from components.auth import render_auth
from components.landing import render_landing
from components.dashboard import render_dashboard
from components.idea_form import render_idea_form
from components.report import render_report

st.set_page_config(page_title="FounderIQ — AI B2B Idea Validation", page_icon="✦", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "view" not in st.session_state:
    st.session_state.view = "landing"
if "ideas" not in st.session_state:
    st.session_state.ideas = []
if "report_idx" not in st.session_state:
    st.session_state.report_idx = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signin"

# The nav's "Sign in" / "Get Started" are plain HTML anchors (not st.button),
# so they can be styled with zero border/background exactly like the design.
# They navigate via a query param, which we read once here and then clear so
# it doesn't keep forcing the view back to "auth" on every later rerun.
_qp = st.query_params
if "view" in _qp:
    st.session_state.view = _qp["view"]
    if "mode" in _qp:
        st.session_state.auth_mode = _qp["mode"]
    st.query_params.clear()


def go_to(view):
    st.session_state.view = view
    st.rerun()


def sign_out():
    st.session_state.user = None
    st.session_state.ideas = []
    st.session_state.view = "landing"
    st.rerun()


def handle_validate(idea, audience, problem):
    if not st.session_state.user:
        st.warning("Sign in to validate your idea.")
        st.session_state.view = "landing"
        return

    with st.spinner("Validating your idea… analyzing market, competitors, and go-to-market fit."):
        try:
            report = validate_idea(idea, audience, problem)
        except Exception as e:
            st.error(f"Something went wrong generating your report: {e}")
            return

    record = {
        "idea": idea,
        "audience": audience,
        "problem": problem,
        "report": report,
        "createdAt": time.time(),
    }
    ideas = get_ideas(st.session_state.user["email"])
    ideas.append(record)
    save_ideas(st.session_state.user["email"], ideas)
    st.session_state.ideas = ideas
    st.session_state.report_idx = len(ideas) - 1
    st.session_state.view = "report"
    st.rerun()


def handle_update_live_signals(data):
    idx = st.session_state.report_idx
    ideas = st.session_state.ideas
    if idx is not None and idx < len(ideas):
        ideas[idx]["liveSignals"] = data
        save_ideas(st.session_state.user["email"], ideas)


# ---------------------------------------------------------------------------
# Top nav
# ---------------------------------------------------------------------------
nav_col1, nav_col2 = st.columns([5, 2])
with nav_col1:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;">'
        '<span class="logo-mark" style="width:30px;height:30px;border-radius:9px;'
        'background:linear-gradient(135deg,#a78bfa,#7c3aed);display:inline-flex;'
        'align-items:center;justify-content:center;font-size:15px;">✦</span> FounderIQ</div>',
        unsafe_allow_html=True,
    )
with nav_col2:
    if st.session_state.user:
        b1, b2, b3 = st.columns([1, 1, 1])
        with b1:
            st.caption(f"👤 {st.session_state.user['name'].split(' ')[0]}")
        with b2:
            if st.button("Dashboard", use_container_width=True):
                go_to("dashboard")
        with b3:
            if st.button("Sign out", use_container_width=True):
                sign_out()
    else:
        st.markdown(
            '<div class="fiq-nav-row">'
            '<a href="?view=auth&mode=signin" target="_self" class="fiq-navlink">Sign in</a>'
            '<a href="?view=auth&mode=signup" target="_self" class="fiq-anchor-btn fiq-anchor-btn-primary">Get Started →</a>'
            '</div>',
            unsafe_allow_html=True,
        )

st.divider()

# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------
if not st.session_state.user:
    if st.session_state.view == "auth":
        render_auth()
    else:
        render_landing(handle_validate)

else:
    if st.session_state.view == "dashboard" or st.session_state.view == "landing":
        render_dashboard(
            st.session_state.ideas or get_ideas(st.session_state.user["email"]),
            on_new_idea=lambda: go_to("newIdea"),
            on_view_report=lambda idx: (st.session_state.__setitem__("report_idx", idx), go_to("report")),
        )
        st.session_state.ideas = get_ideas(st.session_state.user["email"])

    elif st.session_state.view == "newIdea":
        if st.button("← Back to dashboard"):
            go_to("dashboard")
        st.markdown(
            '<div class="fiq-section-title">Validate your idea. <span class="fiq-grad">Get answers in 60s.</span></div>',
            unsafe_allow_html=True,
        )
        render_idea_form(handle_validate, key_prefix="app")

    elif st.session_state.view == "report" and st.session_state.report_idx is not None:
        ideas = st.session_state.ideas or get_ideas(st.session_state.user["email"])
        if st.session_state.report_idx < len(ideas):
            render_report(
                ideas[st.session_state.report_idx],
                st.session_state.report_idx,
                on_back=lambda: go_to("dashboard"),
                on_update_live_signals=handle_update_live_signals,
            )
        else:
            go_to("dashboard")
