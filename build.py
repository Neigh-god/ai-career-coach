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


# app/services/resume_parser.py
w('app/services/resume_parser.py', '''"""Resume parsing service."""
import re
from pathlib import Path
from typing import List, Optional

import pdfplumber
from docx import Document

from app.models.resume import ParsedResume, Education, Experience, Project, Certification


class ResumeParser:
    COMMON_SKILLS = {
        "python", "java", "javascript", "typescript", "sql",
        "django", "flask", "fastapi", "react", "docker",
        "kubernetes", "aws", "git", "machine learning"
    }
    
    @classmethod
    def parse_file(cls, file_path: str) -> ParsedResume:
        path = Path(file_path)
        if path.suffix.lower() == ".pdf":
            raw_text = cls._extract_pdf_text(file_path)
        elif path.suffix.lower() == ".docx":
            raw_text = cls._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        return cls._parse_text(raw_text)
    
    @classmethod
    def _extract_pdf_text(cls, file_path: str) -> str:
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\\n".join(text_parts)
    
    @classmethod
    def _extract_docx_text(cls, file_path: str) -> str:
        doc = Document(file_path)
        return "\\n".join([para.text for para in doc.paragraphs])
    
    @classmethod
    def _parse_text(cls, text: str) -> ParsedResume:
        resume = ParsedResume(raw_text=text)
        resume.name = cls._extract_name(text)
        resume.email = cls._extract_email(text)
        resume.phone = cls._extract_phone(text)
        resume.skills = cls._extract_skills(text)
        return resume
    
    @classmethod
    def _extract_name(cls, text: str) -> Optional[str]:
        lines = text.strip().split("\\n")
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 2 and len(line) < 50 and "@" not in line:
                return line
        return None
    
    @classmethod
    def _extract_email(cls, text: str) -> Optional[str]:
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    @classmethod
    def _extract_phone(cls, text: str) -> Optional[str]:
        pattern = r"(?:\\+?1[-.\\s]?)?\\(?([0-9]{3})\\)?[-.\\s]?([0-9]{3})[-.\\s]?([0-9]{4})"
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    @classmethod
    def _extract_skills(cls, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = []
        for skill in cls.COMMON_SKILLS:
            if skill in text_lower:
                found_skills.append(skill.title())
        return found_skills
''')


# app/services/resume_analyzer.py
w('app/services/resume_analyzer.py', '''"""Resume analysis and ATS scoring."""
from typing import List, Dict
from app.models.resume import ParsedResume, ResumeScore


class ResumeAnalyzer:
    ATS_SECTIONS = ["summary", "experience", "education", "skills", "projects"]
    
    @classmethod
    def analyze(cls, parsed_resume: ParsedResume) -> ResumeScore:
        text = parsed_resume.raw_text.lower()
        section_scores = {}
        
        section_scores["sections"] = cls._score_sections(text)
        section_scores["contact_info"] = cls._score_contact_info(parsed_resume)
        section_scores["skills"] = cls._score_skills(parsed_resume)
        
        overall = sum(section_scores.values())
        strengths = ["Resume parsed successfully"]
        weaknesses = []
        suggestions = ["Add more detail to your resume"]
        
        return ResumeScore(
            overall_score=min(overall, 100),
            section_scores=section_scores,
            missing_sections=[],
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions
        )
    
    @classmethod
    def _score_sections(cls, text: str) -> int:
        score = 0
        for section in cls.ATS_SECTIONS:
            if section in text:
                score += 10
        return min(score, 50)
    
    @classmethod
    def _score_contact_info(cls, resume: ParsedResume) -> int:
        score = 0
        if resume.name: score += 10
        if resume.email: score += 10
        if resume.phone: score += 10
        return score
    
    @classmethod
    def _score_skills(cls, resume: ParsedResume) -> int:
        return min(len(resume.skills) * 5, 30)
''')


# tests/test_services.py
w('tests/test_services.py', '''"""Tests for AI Career Coach."""
import pytest
from app.services.resume_parser import ResumeParser
from app.services.resume_analyzer import ResumeAnalyzer


class TestResumeParser:
    def test_extract_email(self):
        text = "Contact me at john.doe@example.com for more info."
        email = ResumeParser._extract_email(text)
        assert email == "john.doe@example.com"

    def test_extract_skills(self):
        text = "Proficient in Python, SQL, Docker, and AWS."
        skills = ResumeParser._extract_skills(text)
        assert "Python" in skills
        assert "SQL" in skills


class TestResumeAnalyzer:
    def test_score_sections(self):
        text = "Summary\\nExperience\\nEducation\\nSkills\\nProjects"
        score = ResumeAnalyzer._score_sections(text)
        assert score > 0
''')


print("All files created!")
