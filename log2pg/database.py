from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database connection URL, defaulting to a PostgreSQL connection if not provided
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://log2pg:log2pg@db/log2db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Creates a database session and handles its lifecycle.

    Yields:
        Session: A SQLAlchemy Session object connected to the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()