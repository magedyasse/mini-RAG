from pydantic_settings import BaseSettings , SettingsConfigDict
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    
    APP_NAME: str = ""
    API_VERSION: str = ""
    OPENAI_API_KEY: str = ""

    FILE_ALLOWED_TYPES: List[str] = []
    FILE_MAX_SIZE_MB: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int = 1024

    MONGODB_URI: str = ""
    MONGODB_DATABASE: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
            