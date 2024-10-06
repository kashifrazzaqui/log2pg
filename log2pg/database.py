from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .config import DB_CONN_URL

# Database connection URL, defaulting to a PostgreSQL connection if not provided
DATABASE_URL = os.getenv("DATABASE_URL", DB_CONN_URL)

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