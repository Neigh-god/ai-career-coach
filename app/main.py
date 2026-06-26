from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import resume, interview, report
from app.models.database_models import init_db

# Initialize database tables on startup
init_db()

app = FastAPI(
    title="AI Career Coach API",
    description="Backend API for AI Career Coach - Resume analysis, skill gap assessment, interview practice, and career reporting.",
    version="1.0.0"
)

# CORS middleware - allows frontend (Streamlit) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router)
app.include_router(interview.router)
app.include_router(report.router)


@app.get("/")
async def root():
    """Health check / welcome endpoint."""
    return {
        "message": "Welcome to AI Career Coach API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "resume": "/resume",
            "interview": "/interview",
            "report": "/report"
        }
    }


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}