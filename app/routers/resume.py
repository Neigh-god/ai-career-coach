from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import tempfile
import os
from uuid import uuid4

from app.models.resume import ResumeUploadResponse, ParsedResume, ResumeScore
from app.services.resume_parser import ResumeParser
from app.services.resume_analyzer import ResumeAnalyzer

router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)

# In-memory storage for demo (replace with Supabase in production)
_resume_store: dict[str, dict] = {}


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: Optional[str] = None
):
    """
    Upload a resume file (PDF or DOCX), parse it, and analyze it.
    Returns parsed data + ATS score.
    """
    # Validate file type
    allowed_types = [".pdf", ".docx"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Save uploaded file to temp location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Parse the resume
        parsed: ParsedResume = ResumeParser.parse_file(tmp_path)
        
        # Analyze the resume
        score: ResumeScore = ResumeAnalyzer.analyze(parsed)
        
        # Generate resume ID
        resume_id = str(uuid4())
        
        # Store in memory (replace with database later)
        _resume_store[resume_id] = {
            "parsed": parsed,
            "score": score,
            "user_id": user_id
        }
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return ResumeUploadResponse(
            resume_id=resume_id,
            parsed_data=parsed,
            score=score,
            uploaded_at=None  # Will use default datetime if defined in model
        )
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")


@router.get("/{resume_id}")
async def get_resume(resume_id: str):
    """
    Get parsed resume data by ID.
    """
    if resume_id not in _resume_store:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    data = _resume_store[resume_id]
    return {
        "resume_id": resume_id,
        "parsed_data": data["parsed"],
        "score": data["score"]
    }