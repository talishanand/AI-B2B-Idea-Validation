import streamlit as st

EXAMPLES = [
    {
        "idea": "An AI copilot that helps B2B sales teams write personalized outbound emails from CRM signals.",
        "audience": "Series A B2B SaaS SDR teams",
        "problem": "SDRs spend hours writing generic emails that don't convert.",
    },
    {
        "idea": "A Slack bot that automatically summarizes and routes customer support tickets to the right engineer based on past resolutions.",
        "audience": "Engineering-led B2B SaaS companies, 20-200 employees",
        "problem": "Support tickets get misrouted, causing slow resolution times and frustrated customers.",
    },
    {
        "idea": "A compliance automation platform that turns SOC 2 evidence collection into a continuous, always-audit-ready pipeline.",
        "audience": "Series A-C startups pursuing enterprise deals",
        "problem": "SOC 2 prep takes months of manual screenshotting and slows down enterprise sales cycles.",
    },
]


def render_idea_form(on_submit, key_prefix="form"):
    """
    on_submit: callback(idea, audience, problem) called when the user submits.
    key_prefix: unique prefix so this can be rendered more than once per app run.
    """
    if f"{key_prefix}_idea" not in st.session_state:
        st.session_state[f"{key_prefix}_idea"] = ""
        st.session_state[f"{key_prefix}_audience"] = ""
        st.session_state[f"{key_prefix}_problem"] = ""

    st.markdown('<div class="fiq-panel">', unsafe_allow_html=True)

    idea = st.text_area(
        "YOUR IDEA",
        key=f"{key_prefix}_idea",
        placeholder="e.g. An AI copilot that helps B2B sales teams write personalized outbound emails from CRM signals.",
        height=110,
    )
    col1, col2 = st.columns(2)
    with col1:
        audience = st.text_input(
            "TARGET AUDIENCE (OPTIONAL)",
            key=f"{key_prefix}_audience",
            placeholder="e.g. Series A B2B SaaS SDR teams",
        )
    with col2:
        problem = st.text_input(
            "PROBLEM YOU'RE SOLVING (OPTIONAL)",
            key=f"{key_prefix}_problem",
            placeholder="e.g. SDRs spend hours writing generic emails that don't convert",
        )

    footer_col1, footer_col2 = st.columns([2, 1], vertical_alignment="bottom")
    with footer_col1:
        st.caption("Try:")
        ex_cols = st.columns(3)
        for i, ex in enumerate(EXAMPLES):
            if ex_cols[i].button(f"Example {i + 1}", key=f"{key_prefix}_ex_{i}"):
                st.session_state[f"{key_prefix}_idea"] = ex["idea"]
                st.session_state[f"{key_prefix}_audience"] = ex["audience"]
                st.session_state[f"{key_prefix}_problem"] = ex["problem"]
                st.rerun()
    with footer_col2:
        validate_clicked = st.button(
            "✨ Validate idea",
            key=f"{key_prefix}_submit",
            use_container_width=True,
            type="primary",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if validate_clicked:
        current_idea = st.session_state[f"{key_prefix}_idea"].strip()
        if not current_idea:
            st.warning("Describe your idea first.")
        else:
            on_submit(
                current_idea,
                st.session_state[f"{key_prefix}_audience"].strip(),
                st.session_state[f"{key_prefix}_problem"].strip(),
            )
