# ðŸŽ¯ AI Career Coach

> An AI-powered career development platform that helps students and job seekers improve their resumes, prepare for interviews, identify skill gaps, and track their progress over time.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138+-green.svg)

![AI Career Coach Screenshot](screenshot.png)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58+-red.svg)

## âœ¨ Features

- **ðŸ“„ Resume Analyzer** â€” Upload PDF/DOCX, get ATS score, strengths/weaknesses
- **ðŸ” Skill Gap Analysis** â€” Compare skills against 5 target roles
- **ðŸŽ¤ AI Interview Simulator** â€” Technical, HR, Behavioral interviews with evaluation
- **ðŸ“Š Career Report** â€” Combined readiness score + personalized learning roadmap

## ðŸ› ï¸ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | Supabase (planned) |
| Resume Parsing | pdfplumber, python-docx |
| AI | OpenAI API (planned) |

## ðŸ“ Project Structure

## ðŸš€ Quick Start

```bash
# Clone the repo
git clone https://github.com/Neigh-god/ai-career-coach.git
cd ai-career-coach

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend (Terminal 1)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Start frontend (Terminal 2)
streamlit run frontend/app.py
 # ðŸŽ¯ AI Career Coach
...
[all the content]
...
Built with â¤ï¸ using FastAPI + Streamlit
