import streamlit as st
from components.idea_form import render_idea_form

FEATURES = [
    ('''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><line x1="12" y1="7" x2="12" y2="13"/><line x1="10.6" y1="14" x2="6.4" y2="17.6"/><line x1="13.4" y1="14" x2="17.6" y2="17.6"/></svg>''', "VC-grade analysis", "10 sections: SWOT, competitors, revenue model, GTM, risks and more — powered by Claude."),
    ('''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.2"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/></svg>''', "Radar scoring", "7-dimensional validation score with an interactive radar chart. Know exactly where the idea is weakest."),
    ('''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5h16a1 1 0 0 1 1 1V15a1 1 0 0 1-1 1H9.5L5 20v-4H4a1 1 0 0 1-1-1V6.5a1 1 0 0 1 1-1Z"/></svg>''', "Customer discovery", "17 outreach channels with ready-to-send cold email, LinkedIn DM, Reddit post templates."),
    ('''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="5.5" y="4" width="13" height="17" rx="2"/><path d="M9 4V3.3A1.3 1.3 0 0 1 10.3 2h3.4A1.3 1.3 0 0 1 15 3.3V4"/><path d="M9 12.5l1.8 1.8L14.5 10.5"/><line x1="9" y1="17" x2="15" y2="17"/></svg>''', "Execution checklist", "Interview 10 customers → landing page → 100 signups → MVP launch. Track progress in one place."),
    ('''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><polyline points="3,16 9,10 13,14 21,6"/><polyline points="15,6 21,6 21,12"/></svg>''', "Idea comparison", "Save every idea you validate and revisit your dashboard to compare scores over time."),
    ('''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5l7 3V11c0 5-3.2 8.2-7 9.5-3.8-1.3-7-4.5-7-9.5V5.5l7-3Z"/><path d="M9 11.8l2 2 4-4.2"/></svg>''', "Private & yours", "Your ideas are tied to your account only — sign in to keep a private, persistent history."),
]


def render_landing(on_validate):
    st.markdown(
        """
        <div class="fiq-hero">
          <div class="fiq-badge"><span class="fiq-dot"></span> AI B2B Idea Validation</div>
          <h1>Validate your startup idea<br><span class="fiq-grad">in minutes, not weeks.</span></h1>
          <p>FounderIQ generates a VC-grade validation report, a customer discovery playbook across 17 channels,
          and turns analysis into a step-by-step execution checklist.</p>
          <div class="fiq-hero-ctas">
            <a href="#fiq-idea-form" class="fiq-anchor-btn fiq-anchor-btn-primary">Start validating for free →</a>
            <a href="#fiq-features" class="fiq-anchor-btn fiq-anchor-btn-ghost">See how it works</a>
          </div>
          <div class="fiq-tags">10-SECTION REPORT · RADAR SCORING · READY-TO-SEND OUTREACH TEMPLATES</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div id="fiq-features"></div>', unsafe_allow_html=True)
    st.markdown('<div class="fiq-eyebrow">Everything you need</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fiq-section-title">From idea to first customers, <span class="fiq-grad">in one dashboard.</span></div>',
        unsafe_allow_html=True,
    )

    for row_start in range(0, len(FEATURES), 3):
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, FEATURES[row_start:row_start + 3]):
            with col:
                st.markdown(
                    f"""
                    <div class="fiq-card">
                      <div class="fiq-ficon">{icon}</div>
                      <h3>{title}</h3>
                      <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.write("")

    st.markdown(
        """
        <div class="fiq-cta-band">
          <h2>Stop building the wrong thing.</h2>
          <p>Every idea deserves a rigorous 60-second gut-check before you commit six months to it.</p>
          <div style="margin-top:26px;">
            <a href="#fiq-idea-form" class="fiq-anchor-btn fiq-anchor-btn-primary">Validate your first idea →</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div id="fiq-idea-form"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fiq-section-title">Validate your idea. <span class="fiq-grad">Get answers in 60s.</span></div>',
        unsafe_allow_html=True,
    )
    render_idea_form(on_validate, key_prefix="landing")
