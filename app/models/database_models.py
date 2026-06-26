from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Read from .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_career_coach.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ResumeDB(Base):
    __tablename__ = "resumes"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    filename = Column(String)
    raw_text = Column(Text)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    skills = Column(JSON)
    overall_score = Column(Integer)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    suggestions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class InterviewSessionDB(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    category = Column(String)
    status = Column(String, default="in_progress")
    questions = Column(JSON)
    responses = Column(JSON, default=list)
    feedbacks = Column(JSON, default=list)
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class CareerReportDB(Base):
    __tablename__ = "career_reports"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    target_role = Column(String)
    resume_score = Column(Integer)
    skill_coverage = Column(Float)
    interview_score = Column(Float, nullable=True)
    overall_recommendation = Column(Text)
    next_steps = Column(JSON)
    missing_skills = Column(JSON)
    learning_path = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()