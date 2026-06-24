from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from app.models.interview import InterviewSession, InterviewResponse, InterviewFeedback
from app.services.interview_engine import InterviewEngine

router = APIRouter(
    prefix="/interview",
    tags=["interview"]
)

# In-memory session storage (replace with Supabase in production)
_sessions: dict[str, InterviewSession] = {}

engine = InterviewEngine()


class StartInterviewRequest(BaseModel):
    user_id: str
    category: str = "behavioral"  # behavioral, technical, situational
    question_count: int = 3


class SubmitAnswerRequest(BaseModel):
    question_id: str
    user_answer: str


@router.post("/start")
async def start_interview(request: StartInterviewRequest):
    """
    Start a new interview session. Returns session ID and questions.
    """
    try:
        session = engine.create_session(
            user_id=request.user_id,
            category=request.category,
            question_count=request.question_count
        )
        
        # Store session
        _sessions[session.session_id] = session
        
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
async def submit_answer(session_id: str, request: SubmitAnswerRequest):
    """
    Submit an answer to a question in the session.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = _sessions[session_id]
    
    # Find the question
    question = None
    for q in session.questions:
        if q.id == request.question_id:
            question = q
            break
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found in this session")
    
    # Create response
    response = InterviewResponse(
        question_id=request.question_id,
        user_answer=request.user_answer
    )
    session.responses.append(response)
    
    # Evaluate answer
    feedback = engine.evaluate_answer(question, response)
    session.feedbacks.append(feedback)
    
    # Update status if all questions answered
    if len(session.responses) >= len(session.questions):
        session.status = "completed"
        # Calculate overall score
        scores = [f.score for f in session.feedbacks]
        session.overall_score = round(sum(scores) / len(scores), 2)
    
    return {
        "question_id": request.question_id,
        "feedback": {
            "score": feedback.score,
            "strengths": feedback.strengths,
            "improvements": feedback.improvements,
            "model_answer": feedback.model_answer
        },
        "session_status": session.status
    }


@router.get("/{session_id}/feedback")
async def get_feedback(session_id: str):
    """
    Get all feedback for a completed or in-progress session.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = _sessions[session_id]
    
    return {
        "session_id": session_id,
        "status": session.status,
        "overall_score": session.overall_score,
        "total_questions": len(session.questions),
        "answered_questions": len(session.responses),
        "feedbacks": [
            {
                "question_id": f.question_id,
                "score": f.score,
                "strengths": f.strengths,
                "improvements": f.improvements,
                "model_answer": f.model_answer
            }
            for f in session.feedbacks
        ]
    }


@router.get("/{session_id}")
async def get_session(session_id: str):
    """
    Get session details and status.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = _sessions[session_id]
    
    return {
        "session_id": session_id,
        "user_id": session.user_id,
        "status": session.status,
        "total_questions": len(session.questions),
        "answered_questions": len(session.responses),
        "overall_score": session.overall_score,
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "difficulty": q.difficulty,
                "answered": any(r.question_id == q.id for r in session.responses)
            }
            for q in session.questions
        ]
    }