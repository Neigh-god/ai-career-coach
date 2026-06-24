"""Resume parsing service."""
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
        return "\n".join(text_parts)
    
    @classmethod
    def _extract_docx_text(cls, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
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
        lines = text.strip().split("\n")
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 2 and len(line) < 50 and "@" not in line:
                return line
        return None
    
    @classmethod
    def _extract_email(cls, text: str) -> Optional[str]:
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    @classmethod
    def _extract_phone(cls, text: str) -> Optional[str]:
        pattern = r"(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})"
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    @classmethod
    def _extract_skills(cls, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = []
        for skill in cls.COMMON_SKILLS:
            if skill in text_lower:
                found_skills.append(skill.upper())
        return found_skills
