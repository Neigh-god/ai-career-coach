from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4


class InterviewQuestion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    category: str  # e.g., "behavioral", "technical", "situational"
    question: str
    difficulty: str  # e.g., "easy", "medium", "hard"


class InterviewResponse(BaseModel):
    question_id: str
    user_answer: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class InterviewFeedback(BaseModel):
    question_id: str
    score: float = Field(ge=0, le=100)  # 0 to 100
    strengths: str
    improvements: str
    model_answer: str


class InterviewSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    questions: List[InterviewQuestion] = []
    responses: List[InterviewResponse] = []
    feedbacks: List[InterviewFeedback] = []
    status: str = "in_progress"  # or "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    overall_score: Optional[float] = None