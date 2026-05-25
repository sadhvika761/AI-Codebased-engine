"""
Centralised config — reads from environment variables (or .env file).
Import `settings` anywhere instead of sprinkling os.getenv() calls.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Google Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"   # or gemini-2.5-pro

    # Paths
    data_dir: str = "data"
    repos_dir: str = "data/repos"
    embeddings_dir: str = "data/embeddings"

    # ChromaDB
    chroma_persist_dir: str = "data/embeddings"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()