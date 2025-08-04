from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv


class Settings(BaseSettings):
    
    GOOGLE_API_KEY: Optional[str] = None
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "uae-inspection-framework"
    PDF_DATA_DIR: str = "output_reports"

    # Model Config
    TEXT_MODEL: str = "gemini-2.5-flash"
    VISION_MODEL: str = "gemini-2.5-flash"

class Config:
    env_file = ".env"
    extra = "ignore"

load_dotenv()
settings = Settings()