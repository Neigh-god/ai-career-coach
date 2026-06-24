"""Auth helpers."""
from datetime import datetime, timedelta
from jose import jwt
from app.config import get_settings

def create_access_token(data: dict, expires_delta=None):
    s = get_settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, s.SECRET_KEY, algorithm="HS256")
