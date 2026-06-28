from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Optional
import tempfile
import os
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.resume import ResumeUploadResponse, ParsedResume, ResumeScore
from app.models.database_models import get_db, ResumeDB
from app.services.resume_parser import ResumeParser    
from app.services.resume_analyzer import ResumeAnalyzer

router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = [".pdf", ".docx"]


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_ext}'. Allowed: {', '.join(ALLOWED_TYPES)}"
        )

    # Read and validate file size
    try:
        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large ({len(content) / 1024 / 1024:.1f}MB). Maximum allowed: 10MB"
            )

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Parse and analyze
        parsed: ParsedResume = ResumeParser.parse_file(tmp_path)
        score: ResumeScore = ResumeAnalyzer.analyze(parsed)

        resume_id = str(uuid4())

        # Save to database
        db_resume = ResumeDB(
            id=resume_id,
            user_id=user_id or "anonymous",
            filename=file.filename,
            raw_text=parsed.raw_text,
            name=parsed.name,
            email=parsed.email,
            phone=parsed.phone,
            skills=parsed.skills,
            overall_score=score.overall_score,
            strengths=score.strengths,
            weaknesses=score.weaknesses,
            suggestions=score.suggestions
        )
        db.add(db_resume)
        db.commit()

        # Clean up
        os.unlink(tmp_path)

        # FIX: Convert dataclass to dict for response
        parsed_dict = {
            "raw_text": parsed.raw_text,
            "name": parsed.name,
            "email": parsed.email,
            "phone": parsed.phone,
            "skills": parsed.skills,
            "experience": parsed.experience,
            "education": parsed.education,
            "projects": parsed.projects,
            "sections": parsed.sections
        }
        
        score_dict = {
            "overall_score": score.overall_score,
            "section_scores": score.section_scores,
            "missing_sections": score.missing_sections,
            "strengths": score.strengths,
            "weaknesses": score.weaknesses,
            "suggestions": score.suggestions
        }

                # FIX: Convert dataclass to dict for response
        return {
            "resume_id": resume_id,
            "parsed_data": {
                "raw_text": parsed.raw_text,
                "name": parsed.name,
                "email": parsed.email,
                "phone": parsed.phone,
                "skills": parsed.skills,
                "experience": parsed.experience,
                "education": parsed.education,
                "projects": parsed.projects,
                "sections": parsed.sections
            },
            "score": {
                "overall_score": score.overall_score,
                "section_scores": score.section_scores,
                "missing_sections": score.missing_sections,
                "strengths": score.strengths,
                "weaknesses": score.weaknesses,
                "suggestions": score.suggestions
            },
            "uploaded_at": datetime.utcnow()
        }

    except HTTPException:
        raise
    except Exception as e:
        # Clean up temp file if exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")


@router.get("/{resume_id}")
async def get_resume(resume_id: str, db: Session = Depends(get_db)):
    resume = db.query(ResumeDB).filter(ResumeDB.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {
        "resume_id": resume.id,
        "parsed_data": {
            "raw_text": resume.raw_text,
            "name": resume.name,
            "email": resume.email,
            "phone": resume.phone,
            "skills": resume.skills
        },
        "score": {
            "overall_score": resume.overall_score,
            "strengths": resume.strengths,
            "weaknesses": resume.weaknesses,
            "suggestions": resume.suggestions
        }
    }