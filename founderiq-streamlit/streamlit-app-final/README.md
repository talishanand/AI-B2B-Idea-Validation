# FounderIQ (Streamlit)

AI-powered B2B idea validation app — Streamlit port with the same dark
purple design, radar scoring, live customer signal search, and execution
checklist as the original.

## Local setup

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and add your real ANTHROPIC_API_KEY
streamlit run app.py
```

## Structure

```
app.py                      – main entry point, routing between views
.streamlit/
  config.toml                 – dark purple theme base
  secrets.toml.example         – copy to secrets.toml with your API key
lib/
  styles.py                    – injected CSS matching the original design
  storage.py                    – JSON-file persistence (users, saved ideas)
  claude.py                      – Anthropic API calls (validate + live search)
components/
  auth.py                        – sign in / sign up
  landing.py                      – hero, features, CTA band
  idea_form.py                     – reusable idea input
  dashboard.py                      – saved ideas list
  report.py                          – full report, radar chart, live signals
  radar_chart.py                      – Plotly spider chart
data/                                  – JSON files created at runtime
```

## Deploying to Streamlit Community Cloud

1. Push this folder to a GitHub repo
2. Go to share.streamlit.io → **New app** → pick the repo → set main file to `app.py`
3. In the app's **Settings → Secrets**, paste:
   ```toml
   ANTHROPIC_API_KEY = "your-real-key"
   ```
4. Deploy

## ⚠️ Things to know before relying on this in production

1. **Storage is ephemeral.** `lib/storage.py` writes plain JSON files to disk.
   Streamlit Community Cloud's filesystem resets on every reboot/redeploy,
   so saved users and ideas will not persist indefinitely. For real
   persistence, swap `lib/storage.py` for a proper database — Supabase,
   Postgres, or Streamlit's `st.connection` are good options.

2. **Password hashing is basic.** `hashlib.sha256` with no per-user salt is
   fine to demonstrate the auth flow but isn't how you'd store real user
   credentials. Use `bcrypt` or `argon2` (with a salt) for anything real.

3. **Confirm the model name.** `lib/claude.py` uses `"claude-sonnet-4-5"` —
   check console.anthropic.com for the exact current model string your
   account has access to before deploying.

4. **Session state resets on page refresh.** Streamlit's `st.session_state`
   lives only for the current browser session; refreshing the tab logs the
   user out. For persistent login across refreshes, add a cookie-based
   session library (e.g. `streamlit-authenticator` or `extra-streamlit-components`).
