from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")
    DEBUG: bool = os.getenv("DEBUG", False)
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST")

    # LangChain settings
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", False)
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "")
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", False)

    # Anthropic settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
