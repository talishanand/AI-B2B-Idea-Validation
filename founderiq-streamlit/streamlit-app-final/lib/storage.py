"""
Simple JSON-file persistence for demo purposes.

IMPORTANT: Streamlit Community Cloud's filesystem is EPHEMERAL — it resets
whenever the app reboots or redeploys, so users/ideas saved here will not
survive indefinitely. For a real deployment, swap these functions for a real
database (Supabase, Postgres, Firebase, etc.) or use `st.connection`.
"""

import json
import hashlib
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"


def _read_json(path, fallback):
    if not path.exists():
        return fallback
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return fallback


def _write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def hash_password(password: str) -> str:
    # Fine for a demo; use bcrypt/argon2 + per-user salt for real production auth.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_users() -> dict:
    return _read_json(USERS_FILE, {})


def save_users(users: dict):
    _write_json(USERS_FILE, users)


def _ideas_file(email: str) -> Path:
    safe = email.lower().replace("/", "_").replace("\\", "_")
    return DATA_DIR / f"ideas_{safe}.json"


def get_ideas(email: str) -> list:
    return _read_json(_ideas_file(email), [])


def save_ideas(email: str, ideas: list):
    _write_json(_ideas_file(email), ideas)
