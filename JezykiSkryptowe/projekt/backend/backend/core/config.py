from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    SQLITE_DATABASE_URI: str = "sqlite:///./db.sqlite3"
    OPENAI_API_KEY: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    TAVILY_API_KEY: str
    UNSTRUCTURED_API_KEY: str

    UPLOAD_DIR: str = "uploads"
    
    BASE_MODEL: str = "gpt-4o"
    BASE_EMBEDDING: str = "text-embedding-3-small"
    
    


settings = Settings()  # type: ignore
