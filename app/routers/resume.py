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


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    allowed_types = [".pdf", ".docx"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
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
        
        os.unlink(tmp_path)
        
        return ResumeUploadResponse(
            resume_id=resume_id,
            parsed_data=parsed,
            score=score,
            uploaded_at=datetime.utcnow()
        )
        
    except Exception as e:
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