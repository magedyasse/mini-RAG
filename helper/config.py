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


    GENRATION_BACKEND : str = ""
    EMBEDDING_BACKEND : str = ""

   
    OPENAI_API_URL : str = ""    
    COHERE_API_KEY : str = ""

    GENRATION_MODEL_ID : str = ""
    EMBEDDING_MODEL_ID : str = ""
    EMBEDDING_MODEL_SIZE: int = 0
    
    INPUT_DAFAULT_MAX_CHARACTERS : int = 0
    GENERATION_DAFAULT_MAX_TOKENS : int = 0
    GENERATION_DAFAULT_TEMPERATURE: float = 0.0

    VECTOER_DB_BACKEND : str = ""
    VECTOER_DB_PATH : str = ""
    VECTOER_DB_DISTANCE_METHOD : str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
            