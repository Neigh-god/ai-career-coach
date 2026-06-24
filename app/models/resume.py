"""Resume models."""
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
