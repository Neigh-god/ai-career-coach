"""Database connection."""
from supabase import Client, create_client
from app.config import get_settings

_client = None

def get_db():
    global _client
    if _client is None:
        s = get_settings()
        _client = create_client(s.SUPABASE_URL, s.SUPABASE_KEY)
    return _client
