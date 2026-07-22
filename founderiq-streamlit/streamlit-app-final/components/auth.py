import streamlit as st
from lib.storage import get_users, save_users, hash_password


def render_auth():
    """Renders sign-in/sign-up tabs. Sets st.session_state.user on success."""
    st.markdown(
        '<div class="fiq-badge"><span class="fiq-dot"></span> AI B2B Idea Validation</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="fiq-hero"><h1>Welcome to <span class="fiq-grad">FounderIQ</span></h1>'
        "<p>Sign in or create a free account to start validating ideas.</p></div>",
        unsafe_allow_html=True,
    )

    tab_signin, tab_signup = st.tabs(["Sign in", "Sign up"])

    with tab_signin:
        with st.form("signin_form"):
            email = st.text_input("Email", key="signin_email")
            password = st.text_input("Password", type="password", key="signin_password")
            submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")
            if submitted:
                users = get_users()
                email_key = email.strip().lower()
                user = users.get(email_key)
                if not email or not password:
                    st.error("Please enter email and password.")
                elif not user or user["password"] != hash_password(password):
                    st.error("Incorrect email or password.")
                else:
                    st.session_state.user = {"email": email_key, "name": user["name"]}
                    st.session_state.view = "dashboard"
                    st.rerun()

    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Full name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password",
                                       help="At least 6 characters")
            submitted = st.form_submit_button("Create account", use_container_width=True, type="primary")
            if submitted:
                email_key = email.strip().lower()
                if not name.strip() or not email.strip() or not password:
                    st.error("Please fill in every field.")
                elif "@" not in email or "." not in email:
                    st.error("Enter a valid email address.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    users = get_users()
                    if email_key in users:
                        st.error("An account with this email already exists.")
                    else:
                        users[email_key] = {
                            "name": name.strip(),
                            "password": hash_password(password),
                        }
                        save_users(users)
                        st.session_state.user = {"email": email_key, "name": name.strip()}
                        st.session_state.view = "dashboard"
                        st.rerun()
