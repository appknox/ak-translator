from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")
    DEBUG: bool = os.getenv("DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
