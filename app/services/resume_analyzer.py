"""Resume analysis and ATS scoring."""
from typing import List, Dict
from app.models.resume import ParsedResume, ResumeScore

class ResumeAnalyzer:
    ATS_SECTIONS = ["summary", "experience", "education", "skills", "projects", "certifications"]
    
    @classmethod
    def analyze(cls, parsed_resume: ParsedResume) -> ResumeScore:
        text = parsed_resume.raw_text.lower()
        section_scores = {}

        section_scores["sections"] = cls._score_sections(text)
        section_scores["contact_info"] = cls._score_contact_info(parsed_resume)
        section_scores["skills"] = cls._score_skills(parsed_resume)

        overall = sum(section_scores.values())
        
        # Generate real strengths, weaknesses, suggestions
        strengths = cls._generate_strengths(parsed_resume, section_scores)
        weaknesses = cls._generate_weaknesses(parsed_resume, section_scores)
        missing_sections = cls._find_missing_sections(text)
        suggestions = cls._generate_suggestions(weaknesses, missing_sections)

        return ResumeScore(
            overall_score=min(overall, 100),
            section_scores=section_scores,
            missing_sections=missing_sections,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions
        )

    @classmethod
    def _score_sections(cls, text: str) -> int:
        score = 0
        for section in cls.ATS_SECTIONS:
            if section in text.lower():
                score += 8
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

    @classmethod
    def _generate_strengths(cls, resume: ParsedResume, scores: Dict) -> List[str]:
        strengths = []
        
        if resume.name and resume.email:
            strengths.append("Complete contact information provided")
        
        if len(resume.skills) >= 5:
            strengths.append(f"Strong technical skills section with {len(resume.skills)} skills listed")
        elif len(resume.skills) >= 3:
            strengths.append(f"Good skills coverage with {len(resume.skills)} skills")
        
        if scores["sections"] >= 30:
            strengths.append("Well-structured resume with all major sections")
        
        if resume.experience and len(resume.experience) > 0:
            strengths.append("Professional experience section present")
        
        if resume.education and len(resume.education) > 0:
            strengths.append("Education details included")
        
        if resume.projects and len(resume.projects) > 0:
            strengths.append("Projects section adds value to profile")
        
        if not strengths:
            strengths.append("Resume parsed successfully")
        
        return strengths

    @classmethod
    def _generate_weaknesses(cls, resume: ParsedResume, scores: Dict) -> List[str]:
        weaknesses = []
        
        if not resume.name:
            weaknesses.append("Name not detected in resume")
        if not resume.email:
            weaknesses.append("Email address missing")
        if not resume.phone:
            weaknesses.append("Phone number not found")
        
        if len(resume.skills) < 3:
            weaknesses.append("Limited skills listed — consider adding more relevant technologies")
        
        if scores["sections"] < 30:
            weaknesses.append("Some standard resume sections appear to be missing")
        
        if not resume.experience or len(resume.experience) == 0:
            weaknesses.append("No work experience section found")
        
        if not resume.education or len(resume.education) == 0:
            weaknesses.append("Education section not detected")
        
        if not resume.projects or len(resume.projects) == 0:
            weaknesses.append("Consider adding a projects section to showcase practical work")
        
        if len(resume.raw_text.split()) < 100:
            weaknesses.append("Resume appears too short — expand with more details")
        
        return weaknesses

    @classmethod
def _find_missing_sections(cls, text: str) -> List[str]:
    missing = []
    text_lower = text.lower()
    
    # More flexible matching
    has_experience = any(kw in text_lower for kw in ['experience', 'employment', 'work', 'founder', 'co-founder', 'internship'])
    has_education = any(kw in text_lower for kw in ['education', 'academic', 'degree', 'university', 'college', 'school'])
    has_skills = any(kw in text_lower for kw in ['skills', 'technical', 'competencies'])
    has_projects = any(kw in text_lower for kw in ['projects', 'portfolio'])
    has_summary = any(kw in text_lower for kw in ['summary', 'objective', 'profile'])
    has_certifications = any(kw in text_lower for kw in ['certifications', 'certificates'])
    
    if not has_summary:
        missing.append("summary")
    if not has_experience:
        missing.append("experience")
    if not has_education:
        missing.append("education")
    if not has_skills:
        missing.append("skills")
    if not has_projects:
        missing.append("projects")
    if not has_certifications:
        missing.append("certifications")
    
    return missing

    @classmethod
    def _generate_suggestions(cls, weaknesses: List[str], missing_sections: List[str]) -> List[str]:
        suggestions = []
        
        if "summary" in missing_sections:
            suggestions.append("Add a professional summary at the top (2-3 sentences about your expertise)")
        
        if "experience" in missing_sections:
            suggestions.append("Include work experience with bullet points describing achievements")
        
        if "education" in missing_sections:
            suggestions.append("Add your education details (degree, institution, graduation year)")
        
        if "skills" in missing_sections:
            suggestions.append("Create a dedicated skills section listing your technical competencies")
        
        if "projects" in missing_sections:
            suggestions.append("Add a projects section with links to GitHub or live demos")
        
        if "certifications" in missing_sections:
            suggestions.append("List relevant certifications to strengthen your profile")
        
        # Add suggestions based on weaknesses
        for weakness in weaknesses:
            if "too short" in weakness:
                suggestions.append("Expand each section with quantifiable achievements (e.g., 'Improved performance by 20%')")
            if "contact" in weakness.lower() or "email" in weakness.lower() or "phone" in weakness.lower():
                suggestions.append("Ensure contact info is clearly visible at the top of your resume")
            if "skills" in weakness.lower() and "limited" in weakness.lower():
                suggestions.append("Research job descriptions for your target role and match their required skills")
        
        if not suggestions:
            suggestions.append("Great resume! Consider tailoring it for specific job applications")
        
        return suggestions