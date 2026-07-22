CUSTOM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>
:root{
  --bg: #08070c;
  --card: #131019;
  --card-hover: #171320;
  --border: rgba(255,255,255,0.08);
  --border-2: rgba(255,255,255,0.14);
  --muted: #9c98a8;
  --muted-2: #706c7c;
  --purple: #8b5cf6;
  --purple-2: #a78bfa;
  --green: #34d399;
  --amber: #fbbf24;
  --red: #f87171;
}

html, body, [class*="css"]  {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

/* Page background with center glow like the original site */
.stApp{
  background:
    radial-gradient(ellipse 1100px 560px at 50% 12%, rgba(196,161,255,0.12), transparent 60%),
    radial-gradient(ellipse 700px 500px at 100% 10%, rgba(139,92,246,0.08), transparent 60%),
    var(--bg);
}

/* Hide default Streamlit chrome for a cleaner product feel */
#MainMenu, footer, header {visibility: hidden;}

/* ---- Badge ---- */
.fiq-badge{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(139,92,246,0.10);
  border:1px solid rgba(139,92,246,0.30);
  color:#c9bdfb;font-size:13px;font-weight:600;
  padding:7px 16px;border-radius:999px;margin-bottom:20px;
}
.fiq-dot{width:6px;height:6px;border-radius:50%;background:var(--green);
  box-shadow:0 0 8px rgba(52,211,153,0.9); display:inline-block;}

/* ---- Hero ---- */
.fiq-hero{text-align:center; padding: 30px 10px 10px;}
.fiq-hero h1{
  font-size:44px;line-height:1.1;font-weight:800;letter-spacing:-0.02em;margin:0 0 18px;
  color:#f5f4f8;
}
.fiq-grad{
  background:linear-gradient(135deg,#c4b5fd,#8b5cf6 60%,#7c3aed);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.fiq-hero p{color:var(--muted);font-size:16px;line-height:1.6;max-width:620px;margin:0 auto 6px;}
.fiq-tags{color:var(--muted-2);font-size:11.5px;letter-spacing:0.14em;font-weight:600;
  text-transform:uppercase;text-align:center;margin-top:18px;}

/* ---- Section headers ---- */
.fiq-eyebrow{color:var(--purple-2);font-size:12px;font-weight:700;letter-spacing:0.16em;
  text-transform:uppercase;margin-bottom:8px;}
.fiq-section-title{font-size:30px;font-weight:800;letter-spacing:-0.02em;line-height:1.2;margin:0 0 30px;}

/* ---- Feature / generic cards ---- */
.fiq-card{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:22px; height:100%;
}
.fiq-card h3{font-size:16px;margin:10px 0 8px;font-weight:700;color:#f5f4f8;}
.fiq-card p{color:var(--muted);font-size:13.5px;line-height:1.55;margin:0;}
.fiq-ficon{
  width:40px;height:40px;border-radius:10px;
  background:rgba(139,92,246,0.14);border:1px solid rgba(139,92,246,0.25);
  display:flex;align-items:center;justify-content:center;font-size:18px;
}

/* ---- CTA band ---- */
.fiq-cta-band{
  text-align:center;padding:50px 20px;border-top:1px solid var(--border);
  border-bottom:1px solid var(--border); margin: 30px 0;
}
.fiq-cta-band h2{font-size:32px;font-weight:800;letter-spacing:-0.02em;margin:0 0 12px;color:#f5f4f8;}
.fiq-cta-band p{color:var(--muted);font-size:15px;max-width:520px;margin:0 auto;line-height:1.6;}

/* ---- Panels (report sections) ---- */
.fiq-panel{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:22px; margin-bottom:18px;
}
.fiq-panel h3{margin:0 0 12px;font-size:15.5px;font-weight:700;color:#f5f4f8;}
.fiq-panel p{color:var(--muted);font-size:13.5px;line-height:1.6;margin:0 0 10px;}
.fiq-panel ul{margin:0;padding-left:18px;color:var(--muted);font-size:13.5px;line-height:1.8;}

.fiq-swot-box{background:rgba(255,255,255,0.02);border:1px solid var(--border);
  border-radius:10px;padding:12px; margin-bottom:8px;}
.fiq-swot-box h4{margin:0 0 6px;font-size:11.5px;text-transform:uppercase;letter-spacing:0.06em;}

.fiq-risk{border-bottom:1px solid var(--border);padding:10px 0;}
.fiq-risk .t{font-weight:600;font-size:13.5px;color:#f0a3a3;margin-bottom:3px;}
.fiq-risk .m{font-size:13px;color:var(--muted);}

.fiq-competitor{display:flex;gap:10px;padding:10px 0;border-bottom:1px solid var(--border);}
.fiq-competitor .name{font-weight:700;font-size:13px;min-width:110px;}
.fiq-competitor .detail{font-size:12.5px;color:var(--muted);}

.fiq-thread{background:rgba(255,255,255,0.02);border:1px solid var(--border);
  border-radius:12px;padding:14px 16px;margin-bottom:10px;}
.fiq-thread .top{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.fiq-platform-tag{font-size:11px;font-weight:700;color:var(--purple-2);
  background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.28);
  padding:3px 9px;border-radius:999px;}
.fiq-strength-tag{font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;border:1px solid;}
.fiq-thread .title{font-size:13.5px;font-weight:700;margin-bottom:5px;}
.fiq-thread .insight{color:var(--muted);font-size:12.5px;line-height:1.55;margin:0 0 6px;}
.fiq-reply{font-size:12px;color:#dcd9e6;background:rgba(255,255,255,0.03);
  border-left:2px solid var(--purple);padding:6px 10px;border-radius:0 6px 6px 0;margin:0 0 8px;}

/* ---- Score badge ---- */
.fiq-score-circle{
  width:100px;height:100px;border-radius:50%;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin: 0 auto;
}
.fiq-score-circle .num{font-size:26px;font-weight:800;color:#fff;}
.fiq-score-circle .lbl{font-size:9px;color:var(--muted-2);letter-spacing:0.08em;text-transform:uppercase;}

.fiq-pill{
  display:inline-block; font-size:12px;font-weight:700;padding:5px 12px;border-radius:999px;border:1px solid;
}

/* ---- Dashboard idea rows ---- */
.fiq-idea-row{
  background:var(--card);border:1px solid var(--border);border-radius:14px;
  padding:16px 18px;
}
.fiq-idea-row h4{margin:0 0 4px;font-size:14.5px;font-weight:700;color:#f5f4f8;}
.fiq-idea-row p{margin:0;color:var(--muted-2);font-size:12.5px;}

/* ---- Streamlit widget overrides ---- */
.stButton > button{
  border-radius:10px !important; font-weight:600 !important; border:1px solid var(--border-2) !important;
  background: rgba(255,255,255,0.04) !important; color:#e9e7f0 !important;
}
.stButton > button:hover{ background: rgba(255,255,255,0.09) !important; border-color: var(--purple) !important;}

/* Reliable primary-button targeting: Streamlit renders a real kind="primary"
   attribute on the button element when st.button(..., type="primary") is used.
   This does NOT depend on any div-wrapping trick. */
.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] button[kind="primary"]{
  background: linear-gradient(135deg,#a78bfa,#7c3aed) !important;
  color:#fff !important; border:none !important;
  box-shadow:0 6px 20px rgba(124,58,237,0.35) !important;
}
.stButton > button[kind="primary"]:hover{
  box-shadow:0 8px 26px rgba(124,58,237,0.5) !important;
}

/* Plain text nav link (for "Sign in") — no border, no background, just text */
.fiq-navlink{
  color:#d8d5e0 !important; font-size:15px; font-weight:500;
  text-decoration:none !important; padding:8px 4px;
}
.fiq-navlink:hover{ color:#fff !important; }

/* HTML anchor buttons (for hero CTAs / CTA-band button that just scroll the page —
   these don't need Python state, so plain anchors give pixel-accurate styling) */
.fiq-anchor-btn{
  display:inline-flex; align-items:center; gap:8px;
  border-radius:11px; font-weight:600; font-size:16px;
  padding:14px 26px; text-decoration:none !important; cursor:pointer;
}
.fiq-anchor-btn-primary{
  background: linear-gradient(135deg,#a78bfa,#7c3aed) !important;
  color:#fff !important; box-shadow:0 6px 20px rgba(124,58,237,0.35);
}
.fiq-anchor-btn-primary:hover{ box-shadow:0 8px 26px rgba(124,58,237,0.5); }
.fiq-anchor-btn-ghost{
  background: rgba(255,255,255,0.04) !important;
  color:#e9e7f0 !important; border:1px solid var(--border-2);
}
.fiq-anchor-btn-ghost:hover{ background: rgba(255,255,255,0.09) !important; }

.fiq-nav-row{display:flex;justify-content:flex-end;align-items:center;gap:22px;height:100%;}
.fiq-hero-ctas{display:flex;gap:14px;justify-content:center;margin:6px 0 4px;flex-wrap:wrap;}

.stTextInput input, .stTextArea textarea{
  background: rgba(255,255,255,0.03) !important;
  border:1px solid var(--border) !important;
  color:#f5f4f8 !important; border-radius:11px !important;
}

hr{border-color: var(--border) !important;}
</style>
"""
