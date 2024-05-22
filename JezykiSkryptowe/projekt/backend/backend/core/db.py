from sqlmodel import create_engine

from backend.core.config import settings


engine = create_engine(str(settings.SQLITE_DATABASE_URI), echo=True)
