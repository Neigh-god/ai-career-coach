# 🎯 AI Career Coach

&gt; An AI-powered career development platform that helps students and job seekers improve their resumes, prepare for interviews, identify skill gaps, and track their progress over time.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58+-red.svg)

## ✨ Features

- **📄 Resume Analyzer** — Upload PDF/DOCX, get ATS score, strengths/weaknesses
- **🔍 Skill Gap Analysis** — Compare skills against 5 target roles
- **🎤 AI Interview Simulator** — Technical, HR, Behavioral interviews with evaluation
- **📊 Progress Tracking** — Score history, trend analysis, improvement charts
- **📈 Career Report** — Combined readiness score + personalized learning roadmap

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | Supabase (PostgreSQL) |
| Resume Parsing | pdfplumber, python-docx |
| AI | OpenAI API |

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
streamlit run frontend/app.py
