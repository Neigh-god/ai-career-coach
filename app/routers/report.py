from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from uuid import uuid4

from app.services.skill_gap import SkillGapAnalyzer
from app.services.report_generator import ReportGenerator
from app.routers.interview import _sessions as interview_sessions

router = APIRouter(
    prefix="/report",
    tags=["report"]
)

# In-memory report storage (replace with Supabase in production)
_reports: dict[str, dict] = {}

skill_analyzer = SkillGapAnalyzer()
report_generator = ReportGenerator()


class GenerateReportRequest(BaseModel):
    user_id: str
    target_role: str
    resume_score: float
    resume_strengths: List[str]
    resume_weaknesses: List[str]
    current_skills: List[str]
    interview_session_id: Optional[str] = None


@router.post("/generate")
async def generate_report(request: GenerateReportRequest):
    """
    Generate a comprehensive career report combining resume, skill gap, and interview data.
    """
    try:
        # Analyze skill gaps
        skill_gap = skill_analyzer.analyze(
            current_skills=request.current_skills,
            target_role=request.target_role
        )
        
        # Get interview session if provided
        interview_session = None
        if request.interview_session_id:
            if request.interview_session_id not in interview_sessions:
                raise HTTPException(
                    status_code=404,
                    detail="Interview session not found"
                )
            interview_session = interview_sessions[request.interview_session_id]
        
        # Generate the report
        report = report_generator.generate_report(
            user_id=request.user_id,
            target_role=request.target_role,
            resume_score=request.resume_score,
            resume_strengths=request.resume_strengths,
            resume_weaknesses=request.resume_weaknesses,
            skill_gap_result=skill_gap,
            interview_session=interview_session
        )
        
        # Store report
        report_id = str(uuid4())
        _reports[report_id] = {
            "report": report,
            "user_id": request.user_id
        }
        
        # Build response
        response = {
            "report_id": report_id,
            "generated_at": report.generated_at.isoformat(),
            "user_id": report.user_id,
            "target_role": report.target_role,
            "resume_section": {
                "overall_score": report.resume_section.overall_score,
                "strengths": report.resume_section.strengths,
                "weaknesses": report.resume_section.weaknesses,
                "suggestions": report.resume_section.suggestions
            },
            "skill_gap_section": {
                "target_role": report.skill_gap_section.target_role,
                "coverage_percent": report.skill_gap_section.coverage_percent,
                "missing_skills": report.skill_gap_section.missing_skills,
                "learning_path": report.skill_gap_section.learning_path
            },
            "interview_section": None,
            "overall_recommendation": report.overall_recommendation,
            "next_steps": report.next_steps
        }
        
        # Add interview section if available
        if report.interview_section:
            response["interview_section"] = {
                "average_score": report.interview_section.average_score,
                "total_questions": report.interview_section.total_questions,
                "answered_questions": report.interview_section.answered_questions,
                "top_performing_areas": report.interview_section.top_performing_areas,
                "areas_to_improve": report.interview_section.areas_to_improve
            }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.get("/{report_id}")
async def get_report(report_id: str):
    """
    Retrieve a previously generated report.
    """
    if report_id not in _reports:
        raise HTTPException(status_code=404, detail="Report not found")
    
    data = _reports[report_id]
    report = data["report"]
    
    response = {
        "report_id": report_id,
        "generated_at": report.generated_at.isoformat(),
        "user_id": report.user_id,
        "target_role": report.target_role,
        "resume_section": {
            "overall_score": report.resume_section.overall_score,
            "strengths": report.resume_section.strengths,
            "weaknesses": report.resume_section.weaknesses,
            "suggestions": report.resume_section.suggestions
        },
        "skill_gap_section": {
            "target_role": report.skill_gap_section.target_role,
            "coverage_percent": report.skill_gap_section.coverage_percent,
            "missing_skills": report.skill_gap_section.missing_skills,
            "learning_path": report.skill_gap_section.learning_path
        },
        "interview_section": None,
        "overall_recommendation": report.overall_recommendation,
        "next_steps": report.next_steps
    }
    
    if report.interview_section:
        response["interview_section"] = {
            "average_score": report.interview_section.average_score,
            "total_questions": report.interview_section.total_questions,
            "answered_questions": report.interview_section.answered_questions,
            "top_performing_areas": report.interview_section.top_performing_areas,
            "areas_to_improve": report.interview_section.areas_to_improve
        }
    
    return response