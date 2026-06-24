"""Resume analysis and ATS scoring."""
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
            if section in text.lower():
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
