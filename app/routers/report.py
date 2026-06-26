from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy.orm import Session

from app.services.skill_gap import SkillGapAnalyzer
from app.services.report_generator import ReportGenerator
from app.models.database_models import get_db, InterviewSessionDB, CareerReportDB

router = APIRouter(
    prefix="/report",
    tags=["report"]
)

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
async def generate_report(request: GenerateReportRequest, db: Session = Depends(get_db)):
    try:
        # Analyze skill gaps
        skill_gap = skill_analyzer.analyze(
            current_skills=request.current_skills,
            target_role=request.target_role
        )
        
        # Get interview session from database if provided
        interview_session = None
        if request.interview_session_id:
            db_session = db.query(InterviewSessionDB).filter(
                InterviewSessionDB.id == request.interview_session_id
            ).first()
            
            if not db_session:
                raise HTTPException(status_code=404, detail="Interview session not found")
            
            # Convert DB session to model format for report generator
            from app.models.interview import InterviewSession, InterviewQuestion, InterviewResponse, InterviewFeedback
            
            questions = [InterviewQuestion(**q) for q in (db_session.questions or [])]
            responses = [InterviewResponse(**r) for r in (db_session.responses or [])]
            feedbacks = [InterviewFeedback(**f) for f in (db_session.feedbacks or [])]
            
            interview_session = InterviewSession(
                session_id=db_session.id,
                user_id=db_session.user_id,
                questions=questions,
                responses=responses,
                feedbacks=feedbacks,
                status=db_session.status,
                overall_score=db_session.overall_score
            )
        
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
        
        # Save report to database
        report_id = str(uuid4())
        db_report = CareerReportDB(
            id=report_id,
            user_id=request.user_id,
            target_role=request.target_role,
            resume_score=report.resume_section.overall_score,
            skill_coverage=report.skill_gap_section.coverage_percent,
            interview_score=report.interview_section.average_score if report.interview_section else None,
            overall_recommendation=report.overall_recommendation,
            next_steps=report.next_steps,
            missing_skills=report.skill_gap_section.missing_skills,
            learning_path=report.skill_gap_section.learning_path
        )
        db.add(db_report)
        db.commit()
        
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
async def get_report(report_id: str, db: Session = Depends(get_db)):
    db_report = db.query(CareerReportDB).filter(CareerReportDB.id == report_id).first()
    
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    response = {
        "report_id": report_id,
        "generated_at": db_report.created_at.isoformat() if db_report.created_at else None,
        "user_id": db_report.user_id,
        "target_role": db_report.target_role,
        "resume_section": {
            "overall_score": db_report.resume_score,
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        },
        "skill_gap_section": {
            "target_role": db_report.target_role,
            "coverage_percent": db_report.skill_coverage,
            "missing_skills": db_report.missing_skills or [],
            "learning_path": db_report.learning_path or []
        },
        "interview_section": None,
        "overall_recommendation": db_report.overall_recommendation,
        "next_steps": db_report.next_steps or []
    }
    
    if db_report.interview_score is not None:
        response["interview_section"] = {
            "average_score": db_report.interview_score,
            "total_questions": 0,
            "answered_questions": 0,
            "top_performing_areas": [],
            "areas_to_improve": []
        }
    
    return response