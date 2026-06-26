"""Database connection and initialization."""
from app.models.database_models import init_db, get_db

# Initialize tables on import
init_db()


def get_db_session():
    """Get a database session."""
    return next(get_db())
