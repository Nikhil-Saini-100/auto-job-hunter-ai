from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "generate_a_super_secret_key_here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "jobhunter"
    DATABASE_URI: str = "sqlite+aiosqlite:///./jobhunter.db" # Default local

    REDIS_URL: str = "redis://redis:6379/0"

    AI_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    PLAYWRIGHT_HEADLESS: bool = True
    USER_DATA_DIR: str = "./browser_data"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
