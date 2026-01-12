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


    GENERATION_BACKEND : str = ""
    EMBEDDING_BACKEND : str = ""

   
    OPENAI_API_URL : str = ""    
    COHERE_API_KEY : str = ""

    GENERATION_MODEL_ID : str = ""
    EMBEDDING_MODEL_ID : str = ""
    EMBEDDING_MODEL_SIZE: int = 0
    
    INPUT_DEFAULT_MAX_CHARACTERS : int = 0
    GENERATION_DEFAULT_MAX_TOKENS : int = 0
    GENERATION_DEFAULT_TEMPERATURE: float = 0.0

    VECTOR_DB_BACKEND : str = ""
    VECTOR_DB_PATH : str = ""
    VECTOR_DB_DISTANCE_METHOD : str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
            