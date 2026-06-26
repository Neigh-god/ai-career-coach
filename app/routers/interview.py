from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.interview import InterviewSession, InterviewResponse, InterviewFeedback, InterviewQuestion
from app.models.database_models import get_db, InterviewSessionDB
from app.services.interview_engine import InterviewEngine

router = APIRouter(
    prefix="/interview",
    tags=["interview"]
)

engine = InterviewEngine()


class StartInterviewRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    category: str = Field(default="behavioral", pattern="^(behavioral|technical|situational)$")
    question_count: int = Field(default=3, ge=1, le=10)


class SubmitAnswerRequest(BaseModel):
    question_id: str = Field(..., min_length=1)
    user_answer: str = Field(..., min_length=1, max_length=10000)


@router.post("/start")
async def start_interview(request: StartInterviewRequest, db: Session = Depends(get_db)):
    try:
        session = engine.create_session(
            user_id=request.user_id,
            category=request.category,
            question_count=request.question_count
        )
        
        # Save to database
        db_session = InterviewSessionDB(
            id=session.session_id,
            user_id=request.user_id,
            category=request.category,
            status="in_progress",
            questions=[q.model_dump() for q in session.questions]
        )
        db.add(db_session)
        db.commit()
        
        return {
            "session_id": session.session_id,
            "status": session.status,
            "questions": [
                {
                    "id": q.id,
                    "category": q.category,
                    "question": q.question,
                    "difficulty": q.difficulty
                }
                for q in session.questions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@router.post("/{session_id}/answer")
async def submit_answer(session_id: str, request: SubmitAnswerRequest, db: Session = Depends(get_db)):
    if not request.user_answer or not request.user_answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty")
    
    if len(request.user_answer) > 10000:
        raise HTTPException(status_code=413, detail="Answer too long (max 10,000 characters)")
    
    # Get session from database
    db_session = db.query(InterviewSessionDB).filter(InterviewSessionDB.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Find the question
    questions = db_session.questions
    question_data = None
    for q in questions:
        if q.get("id") == request.question_id:
            question_data = q
            break
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Question not found in this session")
    
    # Create response
    responses = db_session.responses or []
    responses.append({
        "question_id": request.question_id,
        "user_answer": request.user_answer,
        "timestamp": datetime.utcnow().isoformat()
    })
    db_session.responses = responses
    
    # Evaluate answer
    question = InterviewQuestion(**question_data)
    response = InterviewResponse(
        question_id=request.question_id,
        user_answer=request.user_answer
    )
    feedback = engine.evaluate_answer(question, response)
    
    # Save feedback
    feedbacks = db_session.feedbacks or []
    feedbacks.append(feedback.model_dump())
    db_session.feedbacks = feedbacks
    
    # Update status
    if len(responses) >= len(questions):
        db_session.status = "completed"
        scores = [f.get("score", 0) for f in feedbacks]
        db_session.overall_score = round(sum(scores) / len(scores), 2) if scores else None
        db_session.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "question_id": request.question_id,
        "feedback": {
            "score": feedback.score,
            "strengths": feedback.strengths,
            "improvements": feedback.improvements,
            "model_answer": feedback.model_answer
        },
        "session_status": db_session.status
    }


@router.get("/{session_id}/feedback")
async def get_feedback(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(InterviewSessionDB).filter(InterviewSessionDB.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    feedbacks = db_session.feedbacks or []
    
    return {
        "session_id": session_id,
        "status": db_session.status,
        "overall_score": db_session.overall_score,
        "total_questions": len(db_session.questions) if db_session.questions else 0,
        "answered_questions": len(db_session.responses) if db_session.responses else 0,
        "feedbacks": feedbacks
    }


@router.get("/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(InterviewSessionDB).filter(InterviewSessionDB.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    questions = db_session.questions or []
    responses = db_session.responses or []
    answered_ids = {r.get("question_id") for r in responses}
    
    return {
        "session_id": session_id,
        "user_id": db_session.user_id,
        "status": db_session.status,
        "total_questions": len(questions),
        "answered_questions": len(responses),
        "overall_score": db_session.overall_score,
        "questions": [
            {
                "id": q.get("id"),
                "question": q.get("question"),
                "difficulty": q.get("difficulty"),
                "answered": q.get("id") in answered_ids
            }
            for q in questions
        ]
    }