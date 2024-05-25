import logging
from sqlmodel import create_engine

from backend.core.config import settings


engine = create_engine(str(settings.SQLITE_DATABASE_URI))
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True
