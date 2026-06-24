from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from app.services.skill_gap import SkillGapResult
from app.models.interview import InterviewFeedback, InterviewSession


@dataclass
class ResumeSection:
    overall_score: float  # 0 to 100
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


@dataclass
class SkillGapSection:
    target_role: str
    coverage_percent: float
    missing_skills: List[str]
    learning_path: List[Dict[str, str]]


@dataclass
class InterviewSection:
    average_score: float
    total_questions: int
    answered_questions: int
    feedback_summary: List[str]
    top_performing_areas: List[str]
    areas_to_improve: List[str]


@dataclass
class CareerReport:
    generated_at: datetime
    user_id: str
    target_role: str
    resume_section: ResumeSection
    skill_gap_section: SkillGapSection
    interview_section: Optional[InterviewSection]
    overall_recommendation: str
    next_steps: List[str]


class ReportGenerator:
    """
    Generates a comprehensive career report combining resume analysis,
    skill gap analysis, and interview performance.
    """
    
    def generate_report(
        self,
        user_id: str,
        target_role: str,
        resume_score: float,
        resume_strengths: List[str],
        resume_weaknesses: List[str],
        skill_gap_result: SkillGapResult,
        interview_session: Optional[InterviewSession] = None
    ) -> CareerReport:
        """
        Build the complete career report from all analysis components.
        """
        
        # Build resume section
        resume_section = ResumeSection(
            overall_score=resume_score,
            strengths=resume_strengths,
            weaknesses=resume_weaknesses,
            suggestions=self._generate_resume_suggestions(resume_weaknesses)
        )
        
        # Build skill gap section
        skill_gap_section = SkillGapSection(
            target_role=skill_gap_result.target_role,
            coverage_percent=skill_gap_result.skill_coverage_percent,
            missing_skills=skill_gap_result.missing_skills,
            learning_path=skill_gap_result.learning_recommendations
        )
        
        # Build interview section if available
        if interview_session and interview_session.feedbacks:
            interview_section = self._build_interview_section(interview_session)
        else:
            interview_section = None
        
        # Generate overall recommendation
        overall_recommendation = self._generate_overall_recommendation(
            resume_score,
            skill_gap_result.skill_coverage_percent,
            interview_section.average_score if interview_section else None
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(
            skill_gap_result.missing_skills,
            resume_weaknesses,
            interview_section.areas_to_improve if interview_section else []
        )
        
        return CareerReport(
            generated_at=datetime.utcnow(),
            user_id=user_id,
            target_role=target_role,
            resume_section=resume_section,
            skill_gap_section=skill_gap_section,
            interview_section=interview_section,
            overall_recommendation=overall_recommendation,
            next_steps=next_steps
        )
    
    def _generate_resume_suggestions(self, weaknesses: List[str]) -> List[str]:
        """Generate actionable suggestions based on resume weaknesses."""
        suggestions = []
        for weakness in weaknesses:
            if "experience" in weakness.lower():
                suggestions.append("Add quantifiable achievements to your work experience (e.g., 'Increased efficiency by 20%').")
            elif "skill" in weakness.lower():
                suggestions.append("Create a dedicated skills section with proficiency levels.")
            elif "education" in weakness.lower():
                suggestions.append("Include relevant certifications or online courses.")
            elif "project" in weakness.lower():
                suggestions.append("Add 2-3 projects with links to GitHub or live demos.")
            else:
                suggestions.append(f"Review and improve: {weakness}")
        
        # Add general suggestions if list is short
        if len(suggestions) < 2:
            suggestions.append("Use action verbs at the start of each bullet point.")
            suggestions.append("Keep your resume to 1-2 pages maximum.")
        
        return suggestions
    
    def _build_interview_section(self, session: InterviewSession) -> InterviewSection:
        """Build interview section from session feedbacks."""
        feedbacks = session.feedbacks
        
        if not feedbacks:
            return InterviewSection(
                average_score=0.0,
                total_questions=len(session.questions),
                answered_questions=0,
                feedback_summary=[],
                top_performing_areas=[],
                areas_to_improve=[]
            )
        
        scores = [f.score for f in feedbacks]
        avg_score = sum(scores) / len(scores)
        
        feedback_summary = [f"Q{i+1}: {f.strengths}" for i, f in enumerate(feedbacks)]
        
        # Find top and bottom areas
        sorted_feedbacks = sorted(feedbacks, key=lambda x: x.score, reverse=True)
        top_performing_areas = [f"Question area (score: {f.score})" for f in sorted_feedbacks[:2]]
        areas_to_improve = [f.improvements for f in sorted_feedbacks[-2:]]
        
        return InterviewSection(
            average_score=round(avg_score, 2),
            total_questions=len(session.questions),
            answered_questions=len(session.responses),
            feedback_summary=feedback_summary,
            top_performing_areas=top_performing_areas,
            areas_to_improve=areas_to_improve
        )
    
    def _generate_overall_recommendation(
        self,
        resume_score: float,
        skill_coverage: float,
        interview_score: Optional[float]
    ) -> str:
        """Generate a personalized overall recommendation."""
        
        if resume_score >= 80 and skill_coverage >= 70:
            if interview_score and interview_score >= 75:
                return "You are well-positioned for your target role. Focus on interview refinement and apply to senior-level positions."
            else:
                return "Strong profile. Practice interviews to match your technical readiness."
        
        elif resume_score >= 60 and skill_coverage >= 50:
            return "Good foundation. Prioritize closing your top 3 skill gaps and polish your resume with quantifiable achievements."
        
        else:
            return "Early stage in your target role preparation. Focus on building core skills through projects and certifications, then revisit your resume."
    
    def _generate_next_steps(
        self,
        missing_skills: List[str],
        resume_weaknesses: List[str],
        interview_improvements: List[str]
    ) -> List[str]:
        """Generate prioritized next steps."""
        steps = []
        
        # Skill-related steps
        if missing_skills:
            steps.append(f"Start learning: {missing_skills[0]} (highest priority skill gap)")
            if len(missing_skills) > 1:
                steps.append(f"Next, focus on: {missing_skills[1]}")
        
        # Resume steps
        if resume_weaknesses:
            steps.append(f"Resume action: {resume_weaknesses[0]}")
        
        # Interview steps
        if interview_improvements:
            steps.append(f"Interview practice: {interview_improvements[0]}")
        
        # General steps
        steps.extend([
            "Schedule 2-3 mock interviews per week",
            "Update your LinkedIn profile to match your resume",
            "Apply to 5-10 jobs that match 60%+ of your current skills"
        ])
        
        return steps[:6]  