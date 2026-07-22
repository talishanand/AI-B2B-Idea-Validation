"""
Gemini API calls for FounderIQ (Streamlit).

Uses Google's `google-genai` SDK. The API key is read from
st.secrets["GEMINI_API_KEY"] (set via .streamlit/secrets.toml locally,
or via the "Secrets" panel in Streamlit Community Cloud's app settings).

Get a free key (no credit card) at https://aistudio.google.com/apikey
"""

import json
import re
import streamlit as st
from google import genai
from google.genai import types

# Confirm current free-tier model availability at https://ai.google.dev/gemini-api/docs/models
MODEL = "gemini-2.5-flash"


def _client() -> genai.Client:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to .streamlit/secrets.toml "
            "locally, or in your Streamlit Cloud app's Settings → Secrets. "
            "Get a free key at https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=api_key)


def _extract_json(text: str) -> dict:
    cleaned = text.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{[\s\S]*\}", cleaned)
    return json.loads(match.group(0) if match else cleaned)


def validate_idea(idea: str, audience: str = "", problem: str = "") -> dict:
    prompt = f"""You are a sharp, experienced B2B venture analyst. Analyze the following startup idea and return ONLY a single valid JSON object (no markdown fences, no preamble, no commentary) matching exactly this schema:

{{
  "overallScore": <integer 0-100>,
  "verdict": "<one punchy sentence, max 18 words>",
  "radar": {{
    "marketSize": <0-100>,
    "competitionAdvantage": <0-100>,
    "problemUrgency": <0-100>,
    "feasibility": <0-100>,
    "revenuePotential": <0-100>,
    "differentiation": <0-100>,
    "gtmFit": <0-100>
  }},
  "executiveSummary": "<3-4 sentences>",
  "marketAnalysis": "<3-5 sentences>",
  "competitors": [ {{"name":"...","strength":"...","weakness":"..."}} ],
  "swot": {{ "strengths": [], "weaknesses": [], "opportunities": [], "threats": [] }},
  "targetCustomer": "<2-3 sentences>",
  "revenueModel": {{ "suggested": "...", "pricingIdeas": [] }},
  "gtmStrategy": "<3-4 sentences>",
  "risks": [ {{"risk":"...","mitigation":"..."}} ],
  "outreachChannels": [ {{"channel":"...","template":"..."}} ],
  "executionChecklist": ["..."]
}}

Idea: {idea}
{"Target audience: " + audience if audience else ""}
{"Problem being solved: " + problem if problem else ""}

Be specific, realistic, and B2B-focused. Base competitor names on real or highly plausible companies in this space. Return ONLY the JSON object."""

    client = _client()
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return _extract_json(response.text)


def fetch_live_signals(idea: str, problem: str = "") -> dict:
    prompt = f"""You are a growth researcher helping a B2B founder find real evidence of demand.

Search the web (use several different search phrasings) for genuine, specific discussions — Reddit threads, Hacker News comments, Indie Hackers posts, niche forum threads, or public X/Twitter threads — where people express the same pain point described below. Prioritize recent, specific, real posts over generic articles.

Idea: {idea}
{"Problem being solved: " + problem if problem else ""}

After searching, return ONLY a single valid JSON object (no markdown fences, no commentary) matching exactly this schema:
{{
  "signalScore": <integer 0-100>,
  "signalSummary": "<1-2 sentence summary>",
  "threads": [
    {{
      "platform": "<Reddit / Hacker News / Indie Hackers / X / forum name>",
      "title": "<short paraphrased title, in your own words>",
      "insight": "<1-2 sentence paraphrase, never a direct quote>",
      "url": "<the real URL you found via search>",
      "strength": "<High, Medium, or Low>",
      "replyAngle": "<one specific, non-salesy sentence for how to engage>"
    }}
  ]
}}
Include up to 6 of the strongest threads you actually found. Never invent a URL. If you find no genuinely relevant real discussions, return an empty threads array and explain why in signalSummary."""

    client = _client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        ),
    )
    return _extract_json(response.text)