from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from pathlib import Path
# Modules
from app.core.config import settings, APP_DIR

db_path = APP_DIR / settings.sqlite_db_path
db_path.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
