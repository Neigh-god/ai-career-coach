"""Tests for AI Career Coach."""
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
        assert "PYTHON" in skills
        assert "SQL" in skills


class TestResumeAnalyzer:
    def test_score_sections(self):
        text = "Summary\nExperience\nEducation\nSkills\nProjects"
        score = ResumeAnalyzer._score_sections(text)
        assert score > 0
