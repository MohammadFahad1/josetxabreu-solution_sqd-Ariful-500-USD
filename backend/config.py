from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Gmail
    gmail_address: str
    gmail_app_password: str

    # OpenAI
    openai_api_key: str

    # Google Sheets
    google_sheets_id: str = ""
    google_service_account_json: str = ""

    # App
    database_url: str = ""  # Set via DATABASE_URL env var
    secret_key: str = "dev-secret-key"
    api_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
