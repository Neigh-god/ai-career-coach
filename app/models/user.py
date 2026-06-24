from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4


class UserProfile(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    email: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserPreferences(BaseModel):
    target_role: Optional[str] = None  # e.g., "Software Engineer", "Data Scientist"
    industry: Optional[str] = None     # e.g., "Tech", "Finance", "Healthcare"
    experience_level: Optional[str] = None  # "entry", "mid", "senior"
    preferred_interview_types: List[str] = []  # e.g., ["behavioral", "technical"]


class CareerGoal(BaseModel):
    goal_id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    target_date: Optional[datetime] = None
    status: str = "active"  # "active", "completed", "paused"


class User(BaseModel):
    profile: UserProfile
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    career_goals: List[CareerGoal] = []
    resume_id: Optional[str] = None  