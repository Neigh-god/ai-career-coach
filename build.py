import os

def w(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

# app/__init__.py
w('app/__init__.py', '')

# app/models/__init__.py
w('app/models/__init__.py', '')

# app/routers/__init__.py
w('app/routers/__init__.py', '')

# app/services/__init__.py
w('app/services/__init__.py', '')

# app/utils/__init__.py
w('app/utils/__init__.py', '')

# tests/__init__.py
w('tests/__init__.py', '')

# app/config.py
w('app/config.py', '''"""Application configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Career Coach"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret"
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
''')

# app/database.py
w('app/database.py', '''"""Database connection."""
from supabase import Client, create_client
from app.config import get_settings

_client = None

def get_db():
    global _client
    if _client is None:
        s = get_settings()
        _client = create_client(s.SUPABASE_URL, s.SUPABASE_KEY)
    return _client
''')

# app/auth.py
w('app/auth.py', '''"""Auth helpers."""
from datetime import datetime, timedelta
from jose import jwt
from app.config import get_settings

def create_access_token(data: dict, expires_delta=None):
    s = get_settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, s.SECRET_KEY, algorithm="HS256")
''')

# app/models/resume.py
w('app/models/resume.py', '''"""Resume models."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None


class Experience(BaseModel):
    company: str
    title: str
    description: Optional[str] = None


class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class Certification(BaseModel):
    name: str
    issuer: Optional[str] = None


class ParsedResume(BaseModel):
    raw_text: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    summary: Optional[str] = None


class ResumeScore(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    section_scores: dict = Field(default_factory=dict)
    missing_sections: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class ResumeUploadResponse(BaseModel):
    resume_id: str
    parsed_data: ParsedResume
    score: ResumeScore
    uploaded_at: datetime
''')

print("Phase 1 complete!")
