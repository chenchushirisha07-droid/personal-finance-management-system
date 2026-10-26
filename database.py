from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use a local SQLite file instead of PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./fintrack_db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()